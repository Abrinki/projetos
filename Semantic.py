import PyPDF2
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extrair_texto_pdf(nome_arquivo):
    texto = ""
    with open(nome_arquivo, 'rb') as arquivo:
        pdf = PyPDF2.PdfReader(arquivo)
        for pagina in range(len(pdf.pages)):
            texto += pdf.pages[pagina].extract_text()
    return texto

def processar_texto(texto):
    nlp = spacy.load("en_core_web_sm")
    return nlp(texto)

def calcular_semelhanca_semantica(doc1, doc2):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([doc1.text, doc2.text])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return similarity[0][0]

arquivo_entrada = input("Insira o arquivo pdf: ")

arquivo_saida1 = input("Insira o primeiro arquivo que deseja comparar: ")
arquivo_saida2 = input("Insira o segundo arquivo que deseja comparar: ")

texto_entrada = extrair_texto_pdf(arquivo_entrada)
texto_saida1 = extrair_texto_pdf(arquivo_saida1)
texto_saida2 = extrair_texto_pdf(arquivo_saida2)

doc_entrada = processar_texto(texto_entrada)
doc_saida1 = processar_texto(texto_saida1)
doc_saida2 = processar_texto(texto_saida2)

semelhanca_1 = calcular_semelhanca_semantica(doc_entrada, doc_saida1)
semelhanca_2 = calcular_semelhanca_semantica(doc_entrada, doc_saida2)

resultados = [(arquivo_saida1, semelhanca_1), (arquivo_saida2, semelhanca_2)]
resultados_ordenados = sorted(resultados, key=lambda x: x[1], reverse=True)

print("\nSemelhança de documentos em ordem decrescente:")
for resultado in resultados_ordenados:
    print(f"Documento: {resultado[0]}, Semelhança: {resultado[1] * 100:.2f}%")