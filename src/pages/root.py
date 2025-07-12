import taipy.gui.builder as tgb

with tgb.Page() as root:
    with tgb.layout("9 2 1"):
        tgb.navbar()
        tgb.text("# Taipy  🛠️ Tools", mode="md")
        tgb.image("./img/logo.png", width="100px", height="100px")
