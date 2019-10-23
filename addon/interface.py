def operator(ot, context):

    layout = ot.layout

    column = layout.column(align=True)

    column.label(text='Details:')
    column.prop(ot, 'straight')

    column.prop(ot, 'split')
    column.prop(ot, 'bevel')
    column.prop(ot, 'bevel_size')

    column.separator()
    column.label(text='General:')
    column.prop(ot, 'amount')
    column.prop(ot, 'width')
    column.prop(ot, 'heigth')

    row = column.row(align=True)
    row.prop(ot, 'depth')
    row.prop(ot, 'uniform', text='', icon='ALIGN_FLUSH')

    column.separator()
    column.label(text='Length X:')
    row = column.row(align=True)
    row.prop(ot, 'length_x_min', text='Min')
    row.prop(ot, 'length_x_max', text='Max')

    column.label(text='Length Y:')
    row = column.row(align=True)
    row.prop(ot, 'length_y_min', text='Min')
    row.prop(ot, 'length_y_max', text='Max')

    column.separator()
    column.label(text='Thickness:')
    row = column.row(align=True)
    row.prop(ot, 'thickness_min', text='Min')
    row.prop(ot, 'thickness_max', text='Max')

    column.label(text='Resolution:')
    column.prop(ot, 'surface')

    column.separator()
    column.label(text='Misc:')
    column.prop(ot, 'seed')

    column.separator()
    row = column.row()
    row.label(text='Up Axis:')
    row.prop(ot, 'up_axis', text='')

    column.separator()


def menu_entry(menu, context):

    if context.mode == 'OBJECT':

        layout = menu.layout

        layout.separator()

        layout.operator('object.pipe_nightmare', text='Pipes', icon='PLUGIN')
