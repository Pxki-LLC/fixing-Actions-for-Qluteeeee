def textbox():
    global maxtext
    maxtext=24*(w//640+1)
    render('rect', arg=(((w - button_size_width) // 2,  ((h - button_size_height) // 2) + (button_size_height - 60), button_size_width,  60), (0, 0, 0), True), bordercolor=forepallete)
    if len(textbox_text)<maxtext:
        colortext=255, 255, 255
    else:
        colortext=255, 0, 0
    render('text', arg=(((w - button_size_width) // 2+10, ((h - button_size_height) // 2) + (button_size_height//4)), colortext), text=textbox_text)
