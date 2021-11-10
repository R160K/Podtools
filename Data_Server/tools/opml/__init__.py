#tools.opml
import general
import engine.signal as signal

HEAD_HREF = "./tools/opml/opml_templates/head.opml"
FOOT_HREF = "./tools/opml/opml_templates/foot.opml"
OUTLINE_TEMPLATE_HREF = "./tools/opml/opml_templates/outline.opml"

head = signal.ValueLoader(HEAD_HREF)
foot = signal.ValueLoader(FOOT_HREF)
outline_template = signal.ValueLoader(OUTLINE_TEMPLATE_HREF)

def make_opml(title, outlines):
    OPML = general.fill_template(head.content, {"title": title})
    
    for o in outlines:
        outline = general.fill_template(outline_template.content, o)
        OPML += outline
    
    OPML += foot.content
    
    OPML = OPML.replace("&", "&amp;")
    
    uOPML = OPML.encode('utf-8', 'ignore')
    return uOPML