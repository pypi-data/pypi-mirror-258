#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ukedown
# Copyright (C) 2017 Stuart Sears
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import xml.etree.ElementTree as etree

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor

# local imports
from . import patterns, translations


class JunkCleaner(Preprocessor):
    """
    just cleans up and returns unicode - essentially strips out the 'smart' characters wordprocessors like to
    use in place of good old proper text. Mostly hyphens and quote characters.
    """

    def run(self, lines):
        return [line.translate(translations.UNICODE_CLEAN_TABLE) for line in lines]


class HeaderProcessor(Preprocessor):
    """
    assume first non-blank line is the song title (plus potentially artist)
    find and replace [] entries, replace with h2 (i.e. ##)
    """

    def __init__(self, markdown_instance=None, pattern=patterns.HEADER):
        super(HeaderProcessor, self).__init__(markdown_instance)
        self.pattern = re.compile(pattern)

    def run(self, lines):
        new_lines = []
        while True:
            # pop first line from the list
            x = lines.pop(0)

            # if it's not blank, then this is what we want
            if x.strip() != "":
                # append it flagged as h1 - remove any existing leading '#' symbols
                new_lines.append("# %s" % x.lstrip("#"))
                break
        new_lines.extend(lines)

        return new_lines


class SectionHeaderProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("span")
        el.attrib["class"] = "section_header"
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class ChordProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("span")
        el.attrib["class"] = "chord"
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class VoxProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("span")
        el.set("class", "vox")
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class NotesProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("span")
        el.set("class", "notes")
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class RepeatsProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("span")
        el.set("class", "repeats")
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class TagProcessor(InlineProcessor):
    """
    wrapper class around pattern replacement
    sets additional attrs, allows us to use the same 'factory'
    for each pattern
    """

    def __init__(self, pattern, markdown_instance=None, tag="span", **attrib):
        super(TagPattern, self).__init__(pattern, markdown_instance)
        self.tag = tag
        self.attrib = attrib

    def handleMatch(self, m):
        el = etree.Element(self.tag)
        if self.attrib:
            for k, v in list(self.attrib.items()):
                if k == "cls":
                    k = "class"
                el.set(k, v)
        el.text = m.group(2)
        return el


class BoxSectionProcessor(BlockProcessor):
    """process the ^| lines representing a box in a chord sheet"""

    def __init__(self, parser, pattern=patterns.BOX):
        super(BoxSectionProcessor, self).__init__(parser)

        self.pattern = re.compile(pattern, re.MULTILINE)

    def test(self, parent, block):
        return self.pattern.search(block)

    def run(self, parent, blocks):
        """
        Process a list of blocks (basically, the document split on '\n\n' strings
        search a block for your regex
        """
        block = blocks.pop(0)
        # ^^ this is a chunk of the file, split on '\n\n'.
        # hopefully we have done this between box sections.
        m = self.pattern.search(block)
        if m:
            # all text before we matched our pattern (in this instance that's lines
            # starting with '|' characters
            before = block[: m.start()]  # Lines before box
            # Pass lines before blockquote in recursively for parsing first.
            # parseblocks just runs every blockprocessor over the block
            self.parser.parseBlocks(parent, [before])
            block = "\n".join([
                self.clean(line)
                for line in block[m.start() :].split("\n")
                if self.pattern.search(line)
            ])
        quote = etree.SubElement(parent, "div", {"class": "box"})
        #    quote.set('class', 'box')
        # Recursively parse block with blockquote as parent.
        # change parser state so blockquotes embedded in lists use p tags
        self.parser.state.set("box")
        # spit block on '\n\n', run all blockprocessors over it and attach output
        # to the provided parent('quote') (in this case a div)
        self.parser.parseChunk(quote, block)

        self.parser.state.reset()

    def clean(self, line):
        """Remove ``|`` from beginning (and possibly end)of a line."""
        m = self.pattern.match(line)
        if line.strip() == "|" or re.match(r"^\| *\|$", line):
            return "\n\n"
        elif m:
            return m.group(2)
        else:
            return line.strip()


class CollapseChildProcessor(Treeprocessor):
    """
    Find specified consecutive tags inside a <div class='box'> elem,
    default tag is 'p'
    replace with
    <div>
    <p>
    p1.text<br />
    ...
    </p>
    </div>
    """

    def __init__(
        self, markdown_instance=None, target="div", tclass="box", child_tag="p"
    ):
        """"""
        super(CollapseChildProcessor, self).__init__(markdown_instance)
        self.target = target
        if tclass is not None:
            self.tclass = set(tclass.split())
        self.child_tag = child_tag

    def run(self, tree):
        # handle the idea that there may be multiple top-level elements
        stack = [tree]
        while stack:
            current = stack.pop()
            # process each element, which may have children of its own
            for elem in current:
                cur_classes = set(elem.get("class", "").split())
                if elem.tag == self.target:
                    if self.tclass is not None:
                        if not self.tclass.issubset(cur_classes):
                            continue
                    # merge all children under a single 'p' container
                    self.mergechildren(elem)

    def mergechildren(self, element):
        """
        merges all child paragraphs into a single para,
        replacing the <p> elements with linebreaks

        Args:
            element (etree.ElementTree.Element) -
            - parent element whose children are to be merged/collapsed

        Kwargs:
            ptag(str): type of element that you wish to create as the
            new 'merged' child. Defaults to 'para'
        """
        # get current children, as we're going to edit in place
        current_children = list(element)
        # create a new child element, to which we will add the
        # content of existing children (and their children)
        # arguably we should just use the first found p
        target = etree.SubElement(element, self.child_tag)
        found = False
        for child in current_children:
            # don't merge headers
            # only merge top-level 'para' entries
            if child.tag != self.child_tag:
                continue
            # the first child provides element text to our new parent 'p'
            if found is False:
                target.text = child.text
                found = True
            else:
                newbr = etree.SubElement(target, "br")
                if len(child.text.strip()) != 0:
                    newbr.tail = child.text

            for i in child:
                target.append(i)

            element.remove(child)


class VoxPostProcessor(Postprocessor):
    """Find all orphaned parens and wrap them as backing vox."""

    def run(self, text: str) -> str:
        """Replace start and end markers with an appropriate span."""
        # get the start and end markers from settings
        return text.replace("(", '<span class="vox">').replace(")", "</span>")


class UkeBookExtension(Extension):
    def __init__(self, **kwargs):
        """
        initialiser, sets config (parameters), runs parent init.
        """
        self.config = {
            "header_pattern": [
                patterns.HEADER,
                "regex matching header elements",
            ],
            "inline_element": ["span", "HTML element for inline items"],
            "chord_pattern": [patterns.CHORD, "regex matching chords"],
            "vox_pattern": [patterns.VOX, "regex matching backing vocals"],
            "notes_pattern": [
                patterns.NOTES,
                "regex matching notes/instructions",
            ],
            "repeats_pattern": [
                patterns.REPEATS,
                "regex matching repeats",
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """
        Adds our custom processors to the current markdown instance

        Args:
            md: markdown instance
        """
        # add our extensions...
        # processors are now executed in descending priority order,
        # md.preprocessors.add('junk_cleaner', JunkCleaner(md), '_begin')
        # currently the first preprocessor has prio 30, we should run first.
        # set an absurdly high priority in case other extensions get in the way
        md.preprocessors.register(JunkCleaner(md), "junk_cleaner", 100)
        md.preprocessors.register(
            HeaderProcessor(md, self.getConfig("header_pattern")), "headers", 11
        )
        md.inlinePatterns.register(
            SectionHeaderProcessor(self.getConfig("header_pattern"), md), "header", 179
        )

        md.inlinePatterns.register(
            ChordProcessor(self.getConfig("chord_pattern"), md),
            "chord",
            178,
        )

        md.inlinePatterns.register(
            VoxProcessor(self.getConfig("vox_pattern"), md), "vox", 177
        )

        md.inlinePatterns.register(
            NotesProcessor(self.getConfig("notes_pattern"), md), "notes", 176
        )

        md.inlinePatterns.register(
            RepeatsProcessor(self.getConfig("repeats_pattern"), md), "repeats", 178
        )

        # block processors
        # md.parser.blockprocessors.register(BoxSectionProcessor(md.parser), 'box', '>empty')
        # parser.blockprocessors.register(EmptyBlockProcessor(parser), 'empty', 100)
        md.parser.blockprocessors.register(BoxSectionProcessor(md.parser), "box", 95)

        # tree processors
        # treeprocessors.register(InlineProcessor(md), 'inline', 20)
        md.treeprocessors.register(CollapseChildProcessor(md), "collapsediv", 15)

        # postprocessing - clean up the final output
        # md.postprocessors.register(VoxPostProcessor(md), "postvox", 90)


def makeExtension(*args, **kwargs):
    return UkeBookExtension(*args, **kwargs)
