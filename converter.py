from line import Line
from lxml.etree import parse, ElementTree
from lxml.builder import E
import pyewts


class Converter:
    def __init__(self, file):
        self.file = file
        self.root = None
        self.lines = []
        self.outtxt = ""
        self.read_file()
        self.done = []
        self.converter = pyewts.pyewts()

    def read_file(self):
        with open(self.file, 'r') as filein:
            self.root = parse(filein).getroot()

    def process_lines(self):
        ln_items = self.root.xpath('/etext/item')
        for i, ln in enumerate(self.root.xpath('/etext/item')):
            self.lines.append(Line(ln))
        for ln in self.lines:
            self.convert_line(ln)

    def get_converted_xml(self):
        xmltxt = E.text(
            E.body(
                E.div1(
                    E.p('')
                )
            )
        )
        p = xmltxt.xpath('/*//p')[0]
        lns = self.lines
        for ln in lns:
            mss = ln.get_milestone()
            last_ms = None
            for ms in mss:
                last_ms = ms
                p.append(ms)
            last_ms.tail = ln.tib
        return xmltxt

    def write_xml(self, fnm):
        xroot = self.get_converted_xml()
        et = ElementTree(xroot)
        et.write(fnm, encoding='utf-8', pretty_print=True)

    def convert_line(self, ln):
        unitib = self.converter.toUnicode(ln.wylie)
        ln.tib = unitib.replace(r'༎', r'།།')  # convert single character double shad into two single shads

