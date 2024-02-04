import ipywidgets as widgets
import NELL.gui.GuiUtils as gui

class ControlCenter:

    def __init__(self):

        self.url_input = gui.new_text_widget('URL Inicial:', 'Digite a URL inicial aqui')
        self.github_repo_input = gui.new_text_widget('Repositório GitHub:', 'Digite o repositório do GitHub aqui')
        self.test_name_input = gui.new_text_widget('Nome do Teste:', 'Nome do Teste')
        self.detailed_description_input = gui.new_textarea_widget('Descrição Detalhada:', 'Descreva o propósito do teste aqui')
        self.test_identifier_input = gui.new_text_widget('Identificador do Cenário:', 'Identificador do Cenário')
        self.tags_input = gui.new_text_widget('Tags/Labels:', 'Tags/Labels separados por vírgula')
        self.generate_details_button = gui.new_button_widget('Gerar Detalhes', 'info', 'magic')
        self.start_button = gui.new_button_widget('Iniciar Gravação', 'success', 'play')
        self.stop_button = gui.new_button_widget('Parar Gravação', 'danger', 'stop')

        self.generate_details_button.on_click(self.generate_details)

        self.content = widgets.VBox(
            self.url_input,
            self.github_repo_input,
            self.detailed_description_input,
            self.generate_details_button,
            self.test_name_input,
            self.test_identifier_input,
            self.tags_input,
            widgets.HBox([self.start_button, self.stop_button])
        )


    def generate_details(self, b):
        # Placeholder para a lógica de auto-preenchimento
        print("Gerando detalhes baseado na descrição...")
