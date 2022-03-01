import wikipedia
wikipedia.set_lang('ru')
articles = ['Северо-Шотландское нагорье','Спейсайд (Тринидад и Тобаго)','Айлей','Кэмпбелтаун']
if __name__ == '__main__':
   for aritcle in articles:
      with open('.\Regions\{}.txt'.format(aritcle),'w',encoding='utf-8') as f:
         f.write(wikipedia.page('{}'.format(aritcle)).content)