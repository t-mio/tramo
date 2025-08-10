import flet as ft


class MapPage:
    def __init__(self,page:ft.Page):
        self.page = page

    def create_page(self):
        content = ft.Container(
        )

        return ft.Stack(
            [
                
                content
            ]
        )


    # page.add(
    #     ft.Text("Click anywhere to add a Marker, long-click to add a CircleMarker."),
    #     map.Map(
    #         expand=True,
    #         initial_center=map.MapLatitudeLongitude(15, 10),
    #         initial_zoom=4.2,
    #         interaction_configuration=map.MapInteractionConfiguration(
    #             flags=map.MapInteractiveFlag.ALL
    #         ),
    #         on_init=lambda e: print(f"Initialized Map"),
    #         on_tap=handle_tap,
    #         on_secondary_tap=handle_tap,
    #         on_long_press=handle_tap,
    #         # on_event=lambda e: print(e),
    #         layers=[
    #             map.TileLayer(
    #                 url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    #                 on_image_error=lambda e: print("TileLayer Error"),
    #             ),

    #         ]))
