import json
import requests
from os import getcwd, path

from pydantic import ValidationError
from .entities.nota_pedido import NotaPedido

from nf_consumo.consumo_service import ConsumoService

class wrapper_jira:
    def __init__(self, jira_api, jira_fields = None):
        self._auth = (jira_api["USERNAME"], jira_api["ACCESS_TOKEN"])
        self._api_issue_url = jira_api["ISSUE_URL"]
        self._api_form_url = jira_api["FORM_URL"]
        self._cloud_id = jira_api["CLOUD_ID"]
        self._jira_fields = jira_fields
        self._api_domain_url = jira_api["DOMAIN_URL"]
        self._set_request()

    def _set_request(self):
        self._api_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self._api_attachment_headers = {
            "Accept": "*/*",
        }
        self._api_atlassian_headers = {
            "Accept": "application/json",
            "X-ExperimentalApi": "opt-in",
        }

    def _remove_null_fields(self, fields):
        fields_data_without_nulls = {}

        for key, value in fields.items():
            if value is not None:
                fields_data_without_nulls[key] = value

        return fields_data_without_nulls
        
    def _rename_fields(self, fields):
        fields = self._fields
        new_fields_data = {}

        for key, value in self._jira_fields.items():
            if value in fields:
                if "text" in fields[value]:
                    new_value = fields[value].get("text")
                elif "date" in fields[value]:
                    new_value = fields[value].get("date")
                elif "value" in fields[value]:
                    new_value = fields[value].get("value")
                else:
                    new_value = fields[value]

                new_fields_data[key] = new_value

        self._fields = new_fields_data

    def _issue_factory(self, issue):

        sintese_itens = []
        validTotalPercents = 0.0

        if not issue['allocation_data']:

            item = {
                'centro': issue['domain_data']['centro']['centro'],
                'centro_custo': f"{issue['domain_data']['centro']['centro']}210",
                'cod_imposto': 'C6',
                'valor_bruto': issue['json_data']['totalInvoiceAmount']
            }

            sintese_item = {
                'categoria_cc': 'K',
                'quantidade': 1,
                'cod_material': issue['domain_data']['fornecedor']['codigo_material'],
                'item': item
            }

            sintese_itens.append(sintese_item)

        else:

            for centro_issue in issue['allocation_data']['centro_custos']:

                validTotalPercents+=float(centro_issue['porcentagem'].replace(',','.'))

                item = {
                    'centro' : centro_issue['nome'].split("210")[0],
                    'centro_custo' : centro_issue['nome'],
                    'cod_imposto' : 'C6',
                    'valor_bruto' : '{:.2f}'.format(issue['json_data']['totalInvoiceAmount'] * float(centro_issue['porcentagem'].replace(',','.')) / 100 , 2)
                }

                sintese_item = {
                    'categoria_cc': 'K',
                    'quantidade': 1,
                    'cod_material': issue['domain_data']['fornecedor']['codigo_material'],
                    'item': item
                }

                sintese_itens.append(sintese_item)

            if validTotalPercents != 100.0:
                raise Exception(f'Invalid total percentage: {validTotalPercents}%')

        anexo = {
            'path' : issue['pdf_data']['path'],
            'filename' : issue['pdf_data']['file_name']
        }

        nota_pedido = {
            'tipo': 'ZCOR',
            'org_compras': 'ORES',
            'grp_compradores': '501',
            'empresa': 'HFNT',
            'cod_fornecedor': issue['domain_data']['fornecedor']['codigo_sap'],
            'sintese_itens': sintese_itens,
            'anexo': anexo          
        }

        return nota_pedido


    def get_nf_issue_context(self, issue_id):
        try:
            #### REQUEST ####
            issue_request = requests.get(
                f"{self._api_issue_url}/issue/{issue_id}",
                headers=self._api_headers,
                auth=self._auth,
            )
            issue_request.raise_for_status()
            issue_data = issue_request.json()

            #### REMOVE NULL FIELDS ####
            issue_data['fields'] = self._remove_null_fields(issue_data.get('fields'))

            ### GET ATTACHMENT ###
            if issue_data.get('fields')['attachment'] is None:
                raise Exception('Could not find attachment')
            
            attachment_id = issue_data.get('fields')['attachment'][0]['id']
            attachment = self._get_nf_issue_attachment(attachment_id)

            ##### GET DOMAIN #####
            ## FORNECEDOR
            cnpj_fornecedor = attachment.get('supplierCnpj')
            fornecedor = self._get_nf_domain('fornecedor', cnpj_fornecedor)

            ## CENTRO
            cnpj_centro = attachment.get('clientCnpj')
            centro = self._get_nf_domain('centro', cnpj_centro)

            domain = {
                'fornecedor': fornecedor,
                'centro': centro
            }

            ##### GET PDF #####
            pdf_data = self._download_pdf(attachment['invoiceFiles'][0])

            ##### GET ALLOCATION #####
            allocation = self._get_allocation(attachment['supplierCnpj'], attachment['clientCnpj'], attachment['contractNumber'])

            ##### FORMAT JSON #####
            issue = {
                'issue_data' : issue_data,
                'json_data'  : attachment,
                'domain_data' : domain,
                'allocation_data' : allocation,
                'pdf_data' : pdf_data
            }

            ##### PARSE JSON #####
            issue_model = self._issue_factory(issue)

            ##### CREATE MODEL #####
            nota_pedido = NotaPedido(**issue_model)
            
            #### SAVE JSON ####
            with open('teste_model.json', "w") as json_file:
                json.dump(nota_pedido.model_dump(), json_file, indent=4)

            return NotaPedido(**issue_model)

        # except ValidationError as ex:
        #     console_message(
        #         f"Error criando fornecedor {str(ex)}\n", "stderr", flush=True
        #     )

        except requests.exceptions.HTTPError as e:
            raise Exception(f"Erro ao receber a Nota Fiscal:\n{e}")

        except Exception as e:
            raise Exception(f"Erro ao receber a Nota Fiscal:\n{e}")

    def _get_nf_issue_attachment(self, attachment_id):
        try:
            attachment_request = requests.get(
                f"{self._api_issue_url}/attachment/content/{attachment_id}",
                headers=self._api_attachment_headers,
                auth=self._auth,
            )
            attachment_request.raise_for_status()
            attachment_data = attachment_request.json()
            
            return attachment_data

        except requests.exceptions.HTTPError as e:
            raise Exception(f"Erro ao receber anexo Jira:\n{e}")

        except Exception as e:
            raise Exception(f"Erro ao receber anexo Jira:\n{e}")
        
    def _get_nf_domain(self, type, cnpj):
        
        try:
            domain_request = requests.get(
                f"{self._api_domain_url}/{'fornecedores' if type == 'fornecedor' else 'centros'}?cnpj={cnpj}"
            )
            domain_request.raise_for_status()
            domain_data = domain_request.json()

            if not domain_data:
                raise Exception('Could not find domain')
        
        except Exception as e:
            raise Exception(f"Erro ao receber {type}:\n{e}")
        
        return domain_data
    
    def _get_allocation(self, cnpj_fornecedor, cnpj_cliente, numero_contrato):
        
        try:

            allocation_request = requests.get(
                f"{self._api_domain_url}/rateio?cnpj_fornecedor={cnpj_fornecedor}&cnpj_hortifruti={cnpj_cliente}&numero_contrato={numero_contrato}"
            )
            allocation_request.raise_for_status()
            allocation_data = allocation_request.json()

        except Exception as e:
            raise Exception(f"Erro ao receber rateio:\n{e}")
        
        return allocation_data
    
    def _download_pdf(self, pdf_path):
        path_dir = path.join(getcwd(), 'output')
        pdf_file = ConsumoService().download_pdf(pdf_path, path_dir)
        file_name = pdf_path.split()[-1]

        file_data = {
            'path': path_dir,
            'file_name': file_name
        }

        return file_data

    # def add_comment(self, issue_id_or_key, message):    #     payload = json.dumps(
    #         {
    #             "body": {
    #                 "content": [
    #                     {
    #                         "content": [
    #                             {
    #                                 "type": "emoji",
    #                                 "attrs": {
    #                                     "shortName": ":robot:",
    #                                     "id": "1f916",
    #                                     "text": "🤖",
    #                                 },
    #                             },
    #                             {"text": f" {message}", "type": "text"},
    #                         ],
    #                         "type": "paragraph",
    #                     }
    #                 ],
    #                 "type": "doc",
    #                 "version": 1,
    #             }
    #         }
    #     )
    #     res = requests.post(
    #         f"{self._api_issue_url}/issue/{issue_id_or_key}/comment",
    #         auth=self._auth,
    #         headers=self._api_headers,
    #         data=payload,
    #     )
    #     res.raise_for_status()

    # def post_transition(self, transition_id, issue_id):
    #     payload = json.dumps(
    #         {
    #             "transition": {"id": transition_id},
    #             "update": {
    #                 "comment": [
    #                     {
    #                         "add": {
    #                             "body": {
    #                                 "content": [
    #                                     {
    #                                         "type": "paragraph",
    #                                         "content": [
    #                                             {
    #                                                 "type": "emoji",
    #                                                 "attrs": {
    #                                                     "shortName": ":robot:",
    #                                                     "id": "1f916",
    #                                                     "text": "🤖",
    #                                                 },
    #                                             },
    #                                             {
    #                                                 "type": "text",
    #                                                 "text": "  comment by Robocorp Assistent using the empty screem",
    #                                             },
    #                                         ],
    #                                     }
    #                                 ],
    #                                 "type": "doc",
    #                                 "version": 1,
    #                             }
    #                         }
    #                     }
    #                 ]
    #             },
    #         }
    #     )
    #     res = requests.post(
    #         f"{self._api_issue_url}/issue/{issue_id}/transitions",
    #         auth=self._auth,
    #         headers=self._api_headers,
    #         data=payload,
    #     )
    #     res.raise_for_status()