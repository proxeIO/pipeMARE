def draw(operator, context):

	layout = operator.layout

	align = True

	column = layout.column(align=align)

	column.label(text='General:')
	column.prop(operator, 'amount', text='Max Pipes')
	column.prop(operator, 'width', text='Region Width')
	column.prop(operator, 'height', text='Region Height')

	column.label(text='Pipe Length:')
	column.prop(operator, 'length_x')
	column.prop(operator, 'length_y')

	column.label(text='Details:')
	column.prop(operator, 'straight')
	column.prop(operator, 'decoration')
	column.prop(operator, 'rail')
	column.prop(operator, 'split')
	column.prop(operator, 'bevel')

	column.separator()

	column.prop(operator, 'preview')

	if operator.preview:

		row = column.row()
		row.prop(operator, 'bounds')
		row.prop(operator, 'pipes')

