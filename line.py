import requests
from lxml.etree import Comment
from lxml.builder import E
from re import match


class Line:
    def __init__(self, lnin):
        self.plnum = lnin[0].text
        self.pg = ''
        self.ln = ''
        m = match(r'(\d+)([ab])(\d+)', self.plnum)
        if m:
            self.pg = m.group(1) + m.group(2)
            self.ln = int(m.group(3))
        self.ms = []
        self.section = lnin[1].text
        self.wylie = massage_wylie(lnin[2].text)
        self.tib = ''
        self.conv_error = ''

    def __str__(self):
        return f"{self.pg}.{self.ln}"

    # Needs to return a list in case it is line one and we need to also include page milestone
    def get_milestone(self):
        if len(self.ms) == 0:   # self.ms may contain a list of optional comment and milestones if already processed
            if self.ln == 1:
                self.ms.append(E.milestone(unit="page", n=str(self.pg)))
            self.ms.append(E.milestone(unit="line", n=str(self.ln)))
            # If there was a conversion problem insert comment about it
            if self.conv_error:
                self.ms.append(Comment("Wylie Conv Errors: \n\t\t" + self.conv_error.replace('line 1:', '', 1)
                                       .replace("\n", " ").replace("line 1:", "\n\t\t")
                                        + "\n\t\tOriginal Wylie: \n\t\t" + self.wylie))
        return self.ms


def massage_wylie(wy):
    if wy and len(wy) > 0:
        wy = wy.replace('/ ', '/_')
    return wy

