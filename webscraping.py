import pandas as pd
import requests
from bs4 import BeautifulSoup


def webscraping():
    dic_produtos = {'modelo': [], 'combustivel': [], 'preco': [], 'ano': [], 'km': [], 'cor': [],
                    'cambio': [], 'cidade': [], 'opcionais': []}
    # ultima_pagina = int(soup.findAll(
    #     'p', class_='label__neutral ids_textStyle_label_small_bold')[2].get_text().strip()) # Use this line to scrape all pages on the site
    ultima_pagina = 145
    pagina_com_erro = 143
    for i in range(pagina_com_erro, ultima_pagina+1):
        try:
            url_pag = f'https://www.icarros.com.br/ache/listaanuncios.jsp?pag={i}&ord=35&sop=nta_17|44|51.1_-kmm_1.1_-esc_4.1_-sta_1.1_'
            proxy = "YOU_NEED_PROXY_TO_SCRAP_THIS_SITE"
            proxies = {"http": proxy, "https": proxy}
            response = requests.get(url_pag, proxies=proxies, verify=False)
            html = response.content.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            produtos = soup.find_all('li', class_=('offer-card'))

            for produto in produtos:

                link_produto = produto.find(
                    'a', class_='offer-card__image-container')
                if link_produto and 'href' in link_produto.attrs:
                    href = link_produto['href']

                    url_produto = f'https://www.icarros.com.br{href}'

                    response_produto = requests.get(
                        url_produto, proxies=proxies, verify=False)
                    if response_produto.status_code == 200:
                        html_produto = response_produto.text
                        soup_produto = BeautifulSoup(
                            html_produto, 'html.parser')

                        # Cidade do Carro
                        cidade = soup_produto.find('span', class_='link')
                        cidade_final = cidade.find('a', title=True).text.strip()

                        # Preço e Modelo
                        modelo = soup_produto.find(
                            'h1', class_='titulo-sm').get_text().strip()
                        preco = soup_produto.find(
                            'h2', class_='preco').get_text().strip()
                        preco_correto = preco.replace('R$', '').replace(' ', '')

                        # Informações gerais
                        dados_do_carro = soup_produto.find_all(
                            'span', class_='destaque')
                        combustivel = soup_produto.find(
                            'ul', class_='listavertical')
                        combustivel_text = combustivel.find('p').text.strip()
                        combustivel_final = combustivel_text.split(',')[0]
                        ano = dados_do_carro[0].text.strip()
                        ano_correto = ano[:4]  # Ano
                        km = dados_do_carro[1].text.strip()  # KM
                        cor = dados_do_carro[2].text.strip()  # Cor
                        cambio = dados_do_carro[3].text.strip()  # Câmbio
                        if cambio == 'manual':
                            cambio = 0
                        else:
                            cambio = 1

                        # Lista opcionais possíveis (Em construção)
                        opcionais = soup_produto.find_all(
                            'p', class_='listaopcionais')
                        todos_opcionais = ['airbag motorista', 'freios ABS',
                                           'airbag passageiro',
                                           'ar-condicionado',
                                           'direção elétrica',
                                           'volante com regulagem de altura',
                                           'travas elétricas',
                                           'cd player com MP3',
                                           'entrada USB',
                                           'vidros elétricos dianteiros',
                                           'limajuste de alturap. traseiro',
                                           'desemb. traseiro', 'alarme',
                                           'câmbio automático',
                                           'ajuste de altura',
                                           'distribuição eletrônica de frenagem,',
                                           'controle de tração',
                                           'retrovisores elétricos',
                                           'piloto automático',
                                           'Kit Multimídia',
                                           'bancos de couro',
                                           'limp. traseiro']

                        valores_opcionais = {
                            opcional: 0 for opcional in todos_opcionais}

                        for p_element in opcionais:

                            texto_opcionais = p_element.get_text().strip()

                            opcionais_individuais = [
                                opc.strip() for opc in texto_opcionais.split(',')]

                            for opcional in opcionais_individuais:
                                if opcional in valores_opcionais:
                                    valores_opcionais[opcional] = 1

                        dic_produtos['modelo'].append(modelo)
                        dic_produtos['combustivel'].append(combustivel_final)
                        dic_produtos['preco'].append(preco)
                        dic_produtos['ano'].append(ano_correto)
                        dic_produtos['km'].append(km)
                        dic_produtos['cor'].append(cor)
                        dic_produtos['cambio'].append(cambio)
                        dic_produtos['cidade'].append(cidade_final)
                        dic_produtos['opcionais'].append(valores_opcionais)

                        print("Modelo:", modelo)
                        print("Combustivel:", combustivel_final)
                        print("Preço:", preco_correto)
                        print("Ano:", ano_correto)
                        print("KM:", km)
                        print("Cor:", cor)
                        print("Câmbio:", cambio)
                        print("Cidade:", cidade_final)
                        print("Opcionais", valores_opcionais)

                        # tempo_aleatorio = random.randint(3, 20)
                        # time.sleep(tempo_aleatorio)

        except Exception as e:
            print(f"Erro na raspagem da página {i}: {e}")
            continue

    todos_opcionais = ['airbag motorista', 'freios ABS', 'airbag passageiro',
                       'ar-condicionado', 'direção elétrica',
                       'volante com regulagem de altura', 'travas elétricas',
                       'cd player com MP3', 'entrada USB',
                       'vidros elétricos dianteiros',
                       'limajuste de alturap. traseiro', 'desemb. traseiro',
                       'alarme',
                       'câmbio automático', 'ajuste de altura',
                       'distribuição eletrônica de frenagem',
                       'controle de tração', 'retrovisores elétricos',
                       'piloto automático', 'Kit Multimídia',
                       'bancos de couro',
                       'limp. traseiro']

    df = pd.DataFrame(dic_produtos)
    for opcional in todos_opcionais:
        df[opcional] = df['opcionais'].apply(lambda x: x.get(opcional, 0))
    df.drop('opcionais', axis=1, inplace=True)
    with open('/home/renato/Projetos_Python/Webscraping/precos_carros.csv', 'a', encoding='utf-8', newline='') as file:
        df.to_csv(file, header=(not file.tell()), index=False, sep=';')

    print("Dados salvos no arquivo CSV.")


webscraping()
