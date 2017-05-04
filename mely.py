import sys
import csv
import math


class Meli(object):

    def __init__(self, source, destiny, invoice, weight):

        # Origem, Destino, Custo da Nota e Peso
        self.source = source
        self.destiny = destiny
        self.invoice = int(invoice)
        self.weight = weight

        # Valor da tabela de rotas para recuperacao da linha na tabela de preco por kg/nome.
        self.idx_kg = ""

        # Valor da tabela 2 (alfandega) de rotas para recuperacao da linha na tabela de preco por kg/nome.
        self.idx_kg_t2 = ""

        # Custo por peso/rota.
        self.kg_price = 0

        # Dicionarios contendo linha na tabela 1 especifica dada rota.
        self.row_kg_price = {}

        # Dicionarios contendo linha na tabela 1 especifica dada rota e indice de kg da tabela de rota.
        self.row_route = {}

        # Dicionarios contendo linha na tabela 2 (alfandega) especifica dada rota.
        self.row_kg_price_t2 = {}

        # Dicionarios contendo linha na tabela 2 (alfandega) especifica dada rota e indice de kg da tabela de rota.
        self.row_route_t2 = {}

        # Fator para utilizar no calculo de icms padrao (tabela1).
        self.icms = 6

        # Subtotal para calculo total durante todo o processo.
        self.subtotal = 0

        # Custo total com taxas e aplicado icms
        self.total = 0

        self.calculate_taxs_table1()
        self.calculate_taxs_table2()

    def calculate_taxs_table1(self):
        self.open_route_csv('tabela', 'rotas.csv')

        # Indice da tabela de rotas utilizado para recuperacao na tabela de preco por kg
        self.idx_kg = self.row_route['kg']

        self.open_kg_price_csv('tabela', 'preco_por_kg.csv')

        # Preco dado o peso passado.
        self.kg_price = float(self.round_value(self.row_kg_price['preco']))

        # Valor do seguro dado origem / destino na tabela de rotas
        insurance = int(self.row_route['seguro'])

        # Valor final de seguro:  valor da nota fiscal * seguro / 100
        final_insurance = self.define_insurance(self.invoice, insurance)

        # Valor do prazo dado origem / destino na tabela de rotas
        deadline = self.row_route['prazo']

        # Valor da taxa fixa dado origem / destino na tabela de rotas
        tax_fixed = float(self.row_route['fixa'])

        # Subtotal : taxa calculada de seguro + taxa fixa dada rota origem / destino.
        self.subtotal =  float(final_insurance) + tax_fixed

        # Subtotal : subtotal atual + (peso * custo do kg)
        self.subtotal = self.subtotal + (float(self.weight) * self.kg_price)

        self.total = round(self.apply_icms(self.subtotal), 2)

        self.show_results('tabela', deadline, self.total)

    def calculate_taxs_table2(self):

    	self.open_route_csv('tabela2', 'rotas.csv')

        # Indice da tabela de rotas utilizado para recuperacao na tabela de preco por kg
        self.idx_kg_t2 = self.row_route_t2['kg']

        # Limite de peso
        limite = self.row_route_t2['limite']

        if (float(self.weight) > float(limite) and limite != '0'):
            self.show_results('tabela2', '-', '-')
        else:
            self.open_kg_price_csv('tabela2', 'preco_por_kg.csv')
        
            # Taxa de alfandega
            alfandega = self.row_route_t2['alfandega']

            # Preco dado o peso passado.
            self.kg_price = float(self.round_value(self.row_kg_price_t2['preco']))

            # Valor do seguro dado origem / destino na tabela de rotas
            insurance = int(self.row_route_t2['seguro'])

            # Valor final de seguro:  valor da nota fiscal * seguro / 100
            final_insurance = self.define_insurance(self.invoice, insurance)

            # Valor do prazo dado origem / destino na tabela de rotas
            deadline = self.row_route_t2['prazo']

            # Subtotal : subtotal atual + (peso * custo do kg)
            self.subtotal = self.subtotal + (float(self.weight) * self.kg_price)

            self.icms = self.row_route_t2['icms']

            self.subtotal = self.apply_alfandega(self.subtotal, alfandega)

            self.total = round(self.apply_icms(self.subtotal), 2)

            self.show_results('tabela2', deadline, self.total)


    '''
        Metodo para abrir pasta/arquivo (tabela de rotas) para leitura.
        Retorno : Dicionario contendo campos/valores da tabela segundo origem e destino passados.

    '''
    def open_route_csv(self, table, archive):
        with open(table + '/' + archive) as csv_file:
            reader = csv.DictReader(csv_file)
            row = self.extract_row_route_csv(reader, table)

    '''
        Metodo para abrir pasta/arquivo (tabela de preco_por_kg) para leitura.
        Retorno : Dicionario contendo campos/valores da tabela segundo origem e destino passados.

    '''
    def open_kg_price_csv(self, table, archive):
        with open(table + '/' + archive) as csv_file:
            reader = csv.DictReader(csv_file)
            row = self.extract_row_kg_price_csv(reader, table)

    '''
        Metodo que realiza extracao de uma linha da tabela referenciada de rotas uma origem e destino passados.
        Retorno : Linha da tabela dado origem / destino
    '''
    def extract_row_route_csv(self, reader, table):
            for row in reader:
                if (self.source == row['origem'] and self.destiny == row['destino']):
                    if (table == 'tabela'):
                        self.row_route = row
                    else:
                    	self.row_route_t2 = row

    '''
        Metodo que realiza extracao de uma linha da tabela referenciada de preco_por_kg dado um indice de kg e valor de peso.
        Retorno : Linha da tabela dado um indice de kg e valor de peso
    '''
    def extract_row_kg_price_csv(self, reader, table):
            for row in reader:
                if not row['final']:
                    if (self.idx_kg == row['nome'] and float(self.weight) >= float(row['inicial'])):
                        if (table == 'tabela'):
                            self.row_kg_price = row
                        else:
                            self.row_kg_price_t2 = row
                else:
                    if (self.idx_kg == row['nome'] and (float(self.weight) >= float(row['inicial']) and float(self.weight) < float(row['final']))):
                        if (table == 'tabela'):
                            self.row_kg_price = row
                        else:
                            self.row_kg_price_t2 = row

    '''
        Metodo que imprime o resultado do calculo final
        Retorno : Tabela utilizada, valor do frete e prazo.
    '''
    def show_results(self, folder, total_value, deadline):
    	print "============================="
    	print "TABELA" + " | " + "PRAZO" + " | " +     "VALOR"
        print folder + " | " + " " +  str(total_value) + "    | " +  str(deadline)

        print "============================="

    '''
        Metodo que calcula o valor do seguro.
        Retorno : Taxa de seguro aplicado.
    '''
    def define_insurance(self, invoice_value, insurance):
        return (float(invoice_value) * float(self.round_value(insurance))) / 100

    '''
        Metodo que calcula o icms.
        Retorno : Taxa ICMS aplicado.
    '''
    def apply_icms(self, subtotal):
        return float(subtotal / float(float(100 - int(self.icms)) / 100))

    '''
        Metodo que calcula o taxa de alfandega.
        Retorno : Taxa Alfandega aplicada.
    '''
    def apply_alfandega(self, subtotal, alfandega):
        print subtotal
    	if (alfandega == '0'):
    	    return float(subtotal / 100)
    	else:
            return float(subtotal / int(alfandega) / 100)

    '''
        Metodo que arredonda o valor para cima e com 2 casas decimais.
        Retorno : Retorna valor arredondado para 2 casas decimais e para cima.
    '''
    def round_value(self, value):
        return "%.2f" % round(math.ceil(float(value)), 2)

    '''
        Metodo que calcula o custo de alfandega
        Retorno : Taxa Alfandega aplicada.
    '''
    def define_customs_tax(subtotal, alfandega):
        return subtotal * (alfandega / 100)

if __name__ == '__main__':
    Meli(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
