from nautobot.core.apps import NavMenuItem, NavMenuGroup, NavMenuTab


menu_items = (
    NavMenuTab(
        name="Plugins",
        groups=[
            NavMenuGroup(name="Nautobot UI", items=[
                NavMenuItem(
                    link='plugins:nautobot_ui_plugin:topology',
                    name="Topology Viewer",
                    permissions=["dcim.view_devices"],
                    buttons=[]
                ),
            ]),
        ],
    ),
)
