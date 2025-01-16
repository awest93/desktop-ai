import flet as ft
from ui.styles import AppStyles

class tets_flet:

    def close_dialog(self, dialog):
        """Закрытие диалогового окна"""
        #dialog.open = False                   # Закрытие диалога
        self.page.close(dialog)

    def show_window_1(self):
        self.page.clean()

        def move_main(e):
            self.show_main_window()

        def move_2(e):
            self.show_window_2()

        def move_3(e):
            self.show_window_3()

        self.main_column.controls= [
            ft.Text("1", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600),
            ft.ElevatedButton(
                "MAIN WINDOW",
                icon=ft.Icons.LOGIN,
                on_click=move_main
            ),
            ft.ElevatedButton(
                "2",
                icon=ft.Icons.LOGIN,
                on_click=move_2
            ),
            ft.ElevatedButton(
                "3",
                icon=ft.Icons.LOGIN,
                on_click=move_3
            )
        ]
        
        self.page.add(self.main_column)
        self.page.update()

    def show_window_2(self):
        self.page.clean()

        def move_main(e):
            self.show_main_window()

        def move_1(e):
            self.show_window_1()

        def move_3(e):
            def close_dlg(e):
                self.close_dialog(dialog)
                self.page._controls.clear()

                def move_main(e):
                    self.show_main_window()

                def move_2(e):
                    self.show_window_2()

                def move_1(e):
                    self.show_window_1()

                self.main_column.controls= [
                    ft.Text("3", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600),
                    ft.ElevatedButton(
                        "MAIN WINDOW",
                        icon=ft.Icons.LOGIN,
                        on_click=move_main
                    ),
                    ft.ElevatedButton(
                        "2",
                        icon=ft.Icons.LOGIN,
                        on_click=move_2
                    ),
                    ft.ElevatedButton(
                        "1",
                        icon=ft.Icons.LOGIN,
                        on_click=move_1
                    )
                ]
                
                self.page.add(self.main_column)
                self.page.update()
                #self.show_window_3()

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"sure?"),
                content=ft.Text(f"really?"),
                actions=[
                    ft.TextButton("Ок.", on_click=close_dlg)
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.open(dialog)

        self.main_column.controls= [
            ft.Text("2", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600),
            ft.ElevatedButton(
                "MAIN WINDOW",
                icon=ft.Icons.LOGIN,
                on_click=move_main
            ),
            ft.ElevatedButton(
                "1",
                icon=ft.Icons.LOGIN,
                on_click=move_1
            ),
            ft.ElevatedButton(
                "3",
                icon=ft.Icons.LOGIN,
                on_click=move_3
            )
        ]
        
        self.page.add(self.main_column)
        self.page.update()

    def show_window_3(self):
        self.page.clean()

        def move_main(e):
            self.show_main_window()

        def move_2(e):
            self.show_window_2()

        def move_1(e):
            self.show_window_1()

        self.main_column.controls= [
            ft.Text("3", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600),
            ft.ElevatedButton(
                "MAIN WINDOW",
                icon=ft.Icons.LOGIN,
                on_click=move_main
            ),
            ft.ElevatedButton(
                "2",
                icon=ft.Icons.LOGIN,
                on_click=move_2
            ),
            ft.ElevatedButton(
                "1",
                icon=ft.Icons.LOGIN,
                on_click=move_1
            )
        ]
        
        self.page.add(self.main_column)
        self.page.update()

    def show_main_window(self):
        self.page.clean()

        def move_1(e):
            self.show_window_1()

        def move_2(e):
            self.show_window_2()

        def move_3(e):
            self.show_window_3()

        self.main_column.controls= [
            ft.Text("MAIN WINDOW", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600),
            ft.ElevatedButton(
                "1",
                icon=ft.Icons.LOGIN,
                on_click=move_1
            ),
            ft.ElevatedButton(
                "2",
                icon=ft.Icons.LOGIN,
                on_click=move_2
            ),
            ft.ElevatedButton(
                "3",
                icon=ft.Icons.LOGIN,
                on_click=move_3
            )
        ]
        
        self.page.add(self.main_column)
        self.page.update()

    def main(self, page: ft.Page):
        self.page = page
        AppStyles.set_window_size(page)
        self.main_column = ft.Column(**AppStyles.MAIN_COLUMN)
        self.show_main_window()

def main():
    """Точка входа в приложение"""
    app = tets_flet()                              # Создание экземпляра приложения
    ft.app(target=app.main)                      # Запуск приложения

if __name__ == "__main__":
    main()    