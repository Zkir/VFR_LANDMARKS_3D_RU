"""
Main Cathedral of the Russian Armed Forces
(c) Zkir 2020
"""
#from zcga import ZCGAContext as ctx


def checkRulesMy(ctx):
    if ctx.getTag("building") != "":

        # align local coordinates so that X matches the longest dimension, and oriented east
        ctx.rotateScope(10.52)

        # we will start from the rectangle and will rebuild the form
        # basing of this very algorithm
        ctx.outerRectangle("mass_model")
        #ctx.nil()

    if ctx.getTag("building:part") == "mass_model":
        ctx.split_x((("~1","belltower_block"),(ctx.scope_sy(), "main_block_pre")))

    if ctx.getTag("building:part") == "belltower_block":
        ctx.scale("'1",ctx.scope_sx())

    if ctx.getTag("building:part") == "main_block_pre":
        ctx.split_x((("~1","apse_pre"), ("~4", "main_block"), ("~1","apse_pre")))

    if ctx.getTag("building:part") == "apse_pre":
        ctx.scale("'1", "'0.3")
        if ctx.current_object.relative_Ox < 0:
            ctx.rotateScope(180)
        ctx.primitiveHalfCircle("apse")

    if ctx.getTag("building:part") == "main_block":
        ctx.split_y((("~1", "entrance"), ("~4", "cube"), ("~1", "entrance")))

    if ctx.getTag("building:part") == "entrance":
        ctx.scale("'0.2","'1")