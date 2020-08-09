"""
OCGA/PY rules example
Gorky Park Rotunda
(c) Zkir 2020
"""

def checkRulesMy(ctx):
    if ctx.getTag("building") != "":
        ctx.setTag("height", 7.25)
        ctx.massModel("mass_model")

    if ctx.getTag("building:part") == "mass_model":

        ctx.setTag("building:colour", "#B0B0B0")
        ctx.setTag("building:material", "plaster")

        ctx.split_z_preserve_roof((("0.75","stilobate"),
                                    ("~9.5", "collonade"),
                                    ("~1.5", "entablement"),
                                    ("~0.3", "cornice"),
                                    ("~4.7", "roof")))

    if ctx.getTag("building:part") == "stilobate":
        ctx.setTag("roof:colour", "#101010")
        ctx.setTag("roof:material", "stone")
        ctx.setTag("building:colour", "#202020")
        ctx.setTag("building:material", "stone")
        ctx.split_z_preserve_roof((("~1", "stilobate1"),
                                   ("~1", "stilobate2"),
                                   ("~1", "stilobate3")))

    if ctx.getTag("building:part") == "roof":

        ctx.setTag("roof:colour", "brown")
        ctx.setTag("roof:material", "metal")
        ctx.setTag("building:colour", "brown")
        ctx.setTag("building:material", "metal")
        ctx.split_z_preserve_roof((("~0.9", "roof1"),
                                   ("~0.5", "roof2"),
                                   ("~2.5", "dome"),
                                   ("~0.3", "roof4")))

    if ctx.getTag("building:part") == "stilobate1":
        pass

    if ctx.getTag("building:part") == "stilobate2":
        ctx.scale("'0.9","'0.9")

    if ctx.getTag("building:part") == "stilobate3":
        ctx.scale("'0.8","'0.8")

    if ctx.getTag("building:part") == "collonade":
        ctx.scale("'0.7", "'0.7")

        ctx.comp_border(ctx.current_object.size/7.3, "column_pre")

    if ctx.getTag("building:part") == "entablement":
        ctx.scale("'0.7", "'0.7")

    if ctx.getTag("building:part") == "cornice":
        ctx.scale("'0.8","'0.8")

    if ctx.getTag("building:part") == "roof1":
        ctx.scale("'0.7","'0.7")

    if ctx.getTag("building:part") == "roof2":
        ctx.scale("'0.65","'0.65")

    if ctx.getTag("building:part") == "dome":
        ctx.scale("'0.6","'0.6")
        roof_height= ctx.getTag("height")-ctx.getTag("min_height")
        ctx.setTag("roof:shape", "dome")
        ctx.setTag("roof:height", roof_height)

    if ctx.getTag("building:part") == "roof4":
        ctx.scale("'0.2","'0.2","'2")
        ctx.translate(0,0,"'-0.7")

    if ctx.getTag("building:part") == "column_pre":
        ctx.scale(ctx.scope_sy(),"'1")
        ctx.scale("'1.2", "'1.2")
        if ctx.current_object.split_index%2 == 0:
            ctx.split_z_preserve_roof((("~1", "column_trunk_pre"), (ctx.scope_sx()/5,"column_top1")))
        else:
            ctx.nil()

    if ctx.getTag("building:part") == "column_trunk_pre":
        ctx.primitiveCircle("column_pre2")

    if ctx.getTag("building:part") == "column_pre2":
        ctx.split_z_preserve_roof((("~1", "column_trunk"), (ctx.scope_sx() / 10, "column_top2")))

    if ctx.getTag("building:part") == "column_trunk":
        ctx.scale("'0.8","'0.8")