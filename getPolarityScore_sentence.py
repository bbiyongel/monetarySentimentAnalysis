{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "# -*- encoding: utf-8 -*-"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import pandas as pd\n",
    "from collections import defaultdict\n",
    "import csv"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "from ekonlpy.sentiment import MPCK\n",
    "mpck = MPCK()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "file_list = os.listdir('data/minutes/txt/')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "20071207 의 ngram 수:  4018\n",
      "20071207 매칭 결과 : \n",
      "NoOfPositiveNgrams :  979\n",
      "NoOfnegativeNgrams :  3039\n",
      "어조지수 :  -0.5126928820308612\n",
      "\n",
      "20180227 의 ngram 수:  7679\n",
      "20180227 매칭 결과 : \n"
     ]
    }
   ],
   "source": [
    "positiveNgram = pd.read_csv('data/res/positive.csv', sep='\\n', header=None, names=['positiveNgram'], encoding='utf-8')\n",
    "negativeNgram = pd.read_csv('data/res/negative.csv', sep='\\n', header=None, names=['negativeNgram'], encoding='utf-8')\n",
    "\n",
    "for file in file_list:\n",
    "    NoOfPositiveNgrams, NoOfnegativeNgrams = 0, 0    \n",
    " \n",
    "    minutes = open('data/minutes/txt/'+file, 'r', encoding='utf-8').read()   \n",
    "    \n",
    "    minutesTokens = mpck.tokenize(minutes)\n",
    "    minutesNgrams = mpck.ngramize(minutesTokens)    \n",
    "    \n",
    "    minutesNgramsTotal = minutesNgrams + minutesTokens\n",
    "    \n",
    "    print(file[3:11], '의 ngram 수: ', len(minutesNgramsTotal))\n",
    "    print(file[3:11], '매칭 결과 : ')\n",
    "    \n",
    "    for mN in minutesNgramsTotal:\n",
    "        for pN in positiveNgram.positiveNgram:\n",
    "            if mN == pN:        \n",
    "                NoOfPositiveNgrams = NoOfPositiveNgrams + 1\n",
    "                break\n",
    "#                 print('Positive match ngram: ')\n",
    "#                 print(mN, '==', pN)\n",
    "        for nN in negativeNgram.negativeNgram:\n",
    "            if mN == nN:        \n",
    "                NoOfnegativeNgrams = NoOfnegativeNgrams + 1\n",
    "                break\n",
    "#                 print('negative match ngram: ')\n",
    "#                 print(mN, '==', nN)\n",
    "    \n",
    "#     for mN, pN, nN in zip(minutesNgrams+minutesTokens, positiveNgram.positiveNgram, negativeNgram.negativeNgram):\n",
    "#         if mN == pN:\n",
    "#             NoOfPositiveNgrams = NoOfPositiveNgrams + 1            \n",
    "#             print('Positive match ngrams: ')\n",
    "#             print(mN, '==', pN)\n",
    "#         elif mN == nN:\n",
    "#             NoOfnegativeNgrams = NoOfnegativeNgrams + 1\n",
    "#             print('negative match ngrams: ')\n",
    "#             print(mN, '==', nN)\n",
    "        \n",
    "    \n",
    "    \n",
    "    # 감성사전과 매칭되는 ngram이 없는 경우\n",
    "    if (NoOfPositiveNgrams + NoOfnegativeNgrams) == 0:\n",
    "        print('매칭되는 ngram 없음 ')\n",
    "        continue\n",
    "    \n",
    "    print('NoOfPositiveNgrams : ', NoOfPositiveNgrams)\n",
    "    print('NoOfnegativeNgrams : ', NoOfnegativeNgrams)\n",
    "    \n",
    "    \n",
    "    polarityScore_sentence = (NoOfPositiveNgrams - NoOfnegativeNgrams)/(NoOfPositiveNgrams + NoOfnegativeNgrams)\n",
    "\n",
    "    print('어조지수 : ', polarityScore_sentence)\n",
    "    print()\n",
    "    \n",
    "    with open('data/res/polarityScore.csv', 'a', encoding='utf-8') as f:\n",
    "        f.write(file[3:11]+\",\"+str(polarityScore_sentence)+'\\n')"
   ]
  },
  {
   "cell_type": "raw",
   "metadata": {},
   "source": [
    "minutesNgramsTotal\n",
    "print(len(minutesNgramsTotal))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0        금리/NNG;인상/NNG;가능성/NNG;금리/NNG;상승/NNG\n",
       "1        fed/NNG;금리/NNG;ff/NNG;금리/NNG;인상/NNG\n",
       "2        지표/NNG;금리/NNG;국고채/NNG;수익률/NNG;오르/VV\n",
       "3         금리/NNG;인상/NNG;이전/NNG;금리/NNG;인상/NNG\n",
       "4             아웃퍼폼/NNG;시장/NNG;수익률/NNG;상회/NNG\n",
       "5             장단기/NNG;금리/NNG;스프레드/NNG;축소/NNG\n",
       "6              대출/NNG;중소기업/NNG;대출/NNG;증가/NNG\n",
       "7              소비자/NNG;물가/NNG;상승률/NNG;상승/NNG\n",
       "8               핵심/NNG;소비자/NNG;물가/NNG;상승/NNG\n",
       "9               채권/NNG;수익률/NNG;상승/NNG;제한/NNG\n",
       "10              원유/NNG;원자재/NNG;가격/NNG;하락/NNG\n",
       "11              국제/NNG;원자재/NNG;가격/NNG;급등/NNG\n",
       "12              둔화/NNG;수출/NNG;증가율/NNG;둔화/NNG\n",
       "13              경제/NNG;성장률/NNG;둔화/NNG;우려/NNG\n",
       "14              경제/NNG;성장률/NNG;소폭/MAG;둔화/NNG\n",
       "15              근원/NNG;소비자/NNG;물가/NNG;상승/NNG\n",
       "16              소비자/NNG;물가/NNG;상승/NNG;압력/NNG\n",
       "17              fed/NNG;ff/NNG;금리/NNG;인상/NNG\n",
       "18               예상/NNG;달리/MAG;금리/NNG;인상/NNG\n",
       "19               금리/NNG;인상/NNG;압력/NNG;강화/NNG\n",
       "20               금리/NNG;인상/NNG;속도/NNG;제한/NNG\n",
       "21               세계/NNG;경제/NNG;성장/NNG;견인/NNG\n",
       "22               세계/NNG;경제/NNG;성장/NNG;둔화/NNG\n",
       "23               회복/NNG;지연/NNG;경기/NNG;회복/NNG\n",
       "24               채권/NNG;금리/NNG;상승/NNG;위험/NNG\n",
       "25               해외/NNG;증권/NNG;투자/NNG;급증/NNG\n",
       "26               발행/NNG;cd/NNG;금리/NNG;상승/NNG\n",
       "27               경기/NNG;선행/NNG;지수/NNG;하락/NNG\n",
       "28               경상/NNG;적자/NNG;재정/NNG;적자/NNG\n",
       "29               금리/NNG;인상/NNG;위안/NNG;절상/NNG\n",
       "                        ...                 \n",
       "60020                               계약예규/NNG\n",
       "60021                                정사유/NNG\n",
       "60022                                 금별/NNG\n",
       "60023                                장체계/NNG\n",
       "60024                          지방도시계획위원회/NNG\n",
       "60025                             분산원장기술/NNG\n",
       "60026                                 격담/NNG\n",
       "60027                                새로워질/VA\n",
       "60028                                 한울/NNG\n",
       "60029                                 일죄/NNG\n",
       "60030                                  徒/NNG\n",
       "60031                                  過/NNG\n",
       "60032                               택지지역/NNG\n",
       "60033                                펼쳐나갔/VV\n",
       "60034             금리/NNG;상승/NNG;절반/NNG;되돌/VV\n",
       "60035                거주자/NNG;외화예금/NNG;최대/NNG\n",
       "60036                   정책/NNG;금융/NNG;완화/NNG\n",
       "60037                                 명증/NNG\n",
       "60038                               개미구멍/NNG\n",
       "60039                                전문학/NNG\n",
       "60040                                 성단/NNG\n",
       "60041                                 파벽/NNG\n",
       "60042                                 破僻/NNG\n",
       "60043                                 飛去/NNG\n",
       "60044                                 금릉/NNG\n",
       "60045                                 흥한다/VV\n",
       "60046                               제안제도/NNG\n",
       "60047                   자금/NNG;수요/NNG;축소/NNG\n",
       "60048                     높/VA;등급/NNG;하향/NNG\n",
       "60049                                 혁안/NNG\n",
       "Name: positiveNgram, Length: 60050, dtype: object"
      ]
     },
     "execution_count": 28,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "positiveNgram.positiveNgram"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.series.Series'>\n",
      "yes\n"
     ]
    }
   ],
   "source": [
    "tmp = '성단/NNG'\n",
    "print(type(positiveNgram.positiveNgram))\n",
    "fn = positiveNgram.positiveNgram.str.find(tmp)\n",
    "for pN in positiveNgram.positiveNgram:\n",
    "    if tmp == pN:\n",
    "        print('yes')\n",
    "\n",
    "# if positiveNgram.positiveNgram.str.find(tmp):\n",
    "#     print('yes')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
