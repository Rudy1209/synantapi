from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import WordSerializer
import pandas as pd
import nltk
from nltk.corpus import wordnet
import re

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

bad_words_df = pd.read_csv(r'synonym_antonym_api\badwords.csv', header=None, names=['Word'])
bad_words_set = set(bad_words_df['Word'].str.lower())

df = pd.read_csv(r'synonym_antonym_api\cleaned_education_data.csv')
all_words = set(" ".join(df['CleanedText']).split())

def get_synonyms_antonyms(word):
    synonyms = []
    antonyms = []

    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())

    synonyms = list(set(synonyms))
    antonyms = list(set(antonyms))

    return synonyms, antonyms

def is_bad_word(word):
    return word.lower() in bad_words_set

class WordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        word = request.query_params.get('word')
        if not word:
            return Response({"error": "Word parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)
        if is_bad_word(word):
            return Response({"error": "The entered word is a bad word. Please enter a different word."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            synonyms, antonyms = get_synonyms_antonyms(word)
            li3 = [w for w in synonyms if w in all_words]
            li4 = [w for w in antonyms if w in all_words]
            return Response({
                "word": word,
                "synonyms": li3,
                "antonyms": li4
            })

    def post(self, request):
        try:
            serializer = WordSerializer(data=request.data)
            if serializer.is_valid():
                word = serializer.validated_data['word']
                if is_bad_word(word):
                    return Response({"error": "The entered word is a bad word. Please enter a different word."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    synonyms, antonyms = get_synonyms_antonyms(word)
                    li3 = [w for w in synonyms if w in all_words]
                    li4 = [w for w in antonyms if w in all_words]
                    return Response({
                        "word": word,
                        "synonyms": li3,
                        "antonyms": li4
                    })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
