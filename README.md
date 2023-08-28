## ISSN API  
Библиотека реализует API, который возвращает данные публикации по ISSN.
Даныне по ISSN беруться из официального ISSN API (https://issn.org/).

### **Параметры**:
- issn - Идентификатор ISSN;

### **Возвращает**:
- Словарь с данными по ISSN;


### **Формат возвращаемых данных ISSN**: 
```
{'issn': issn,
 'data': {},
 'unparsed_keys': [],
 'unsuccessful': [],
 'errors': [],
 'stats': {}}
```

### **Описание возвращаемых данных**:
- Тип: Dictionary;
- Возвращает: Словарь с данными об издании (публикации);

1) **issn** - идентификатор ISSN. (Тип string);
2) **data** - информация об издании (публикации). Данные полученные при распознавании ключей `@id`, которые находяться под ключом `@graph`. (Тип dictionary);  
Описание данных издания, в 'data': 

   1. **Country** - название страны, в которой было опубликовано издание; (Тип string);  
   **URI pattern**: `http://id.loc.gov/vocabulary/countries/{country_code}`;
   2. **CountryCode** - код страны; (Тип string);  
   **URI pattern**: `http://issn.org/resource/ISSN/{ISSN}#ReferencePublicationEvent`;

   3. **Organization** - код организации, которая опубликовала издание; (Тип string);   
   **URI pattern**: `http://issn.org/organization/ISSNCenter#{center_code}`;

   4. **ISSN / ISSN_resource** - идентификатор издания, которое находиться на определенном носителе; (Тип string);  
   **URI pattern (ISSN)**: `http://issn.org/resource/ISSN/{ISSN}#ISSN`;
   **URI pattern (ISSN_resource)**: http://issn.org/resource/ISSN/{ISSN}`;

   5. **ISSN-L** - идентификатор издания, обозначающий что здание находится на разных носителях; (Тип string);  
   **URI pattern**: `http://issn.org/resource/ISSN/{ISSN}#ISSN-L`;

   6. **KeyTitle** - ключевое название, по которому идентифицируется издание; (Тип string);  
   **URI pattern**: `http://issn.org/resource/ISSN/{ISSN}#KeyTitle`; 

   7. **resource** - дополнительные данные издания. (Тип dictionary);  
   **URI pattern**: `http://issn.org/resource/ISSN/{ISSN}`; 

      * Описание дополнительных данных издания в 'resource':
        - **URL** - сайт издания. (Тип string);
        - **Name** - перечень названий данного издания. (Тип string);
        - **Title** - это свойство относится к идентификатору KeyTitle, который идентифицирует это издание. (Тип string);
        - **Format** - формат носителя на котором находится данное издание. (Тип string/dictionary);
        - **OtherPhysicalFormat** - это свойство указывает на идентификатор ISSN, идентифицирующий это же издание, но на другом носителе. (Тип string);
        - **IsFormatOf** - это свойство указывает на идентификатор ISSN, идентифицирующий это же издание, но на другом носителе. (Тип string);
        - **IsPartOf** - это свойство относится к ISSN-L, являющемуся частью данного ISSN. (Тип string);
        - **IdentifiedBy** - это свойство относится к идентификаторам ISSN-L и KeyTitle, идентифицирующим данное издание. (Тип string);
        - **MainTitle** - список основных заглавий издания. (Тип string);

4) **unparsed_keys** - список ключей, которые не были включены в возвращаемые данные по ISSN. (Тип list);  

    * Список ключей:
      - resource/ISSN-L/{issn-L}
      - resource/ISSN/{issn}#InterveningPublicationEvent
      - resource/ISSN/{issn}#PublicationPlace
      - resource/ISSN/{issn}#ReproductionPlace
      - resource/ISSN/{issn}#Publisher
      - resource/ISSN/{issn}#IssuingBody
      - resource/ISSN/{issn}#ReproductionAgency
      - organization/keepers#{keeperCode}
      - resource/ISSN/{issn}#PublicationPlace-{placename}-GeoCoordinates
      - resource/ISSN/{issn}#ReproductionPlace-{placeName}-Geocoordinates
      - resource/ISSN/{issn}#CODEN
      - resource/ISSN/{issn}#AbbreviatedKeyTitle
      - resource/ISSN/{issn}#LatestPublicationEvent 

5) **unsuccessful** - список ключей, которые не были успешно распознаны. (Тип list);
6) **errors** - список ошибок, которые могли возникнуть в результате запроса к ISSN API (https://issn.org/). (Тип list):
   1. Отсутствие подключения интернета;
   2. Некорректный запрос на получение данных из сети;
   3. Некорректный формат данных, полученных из сети;

7) **stats** - данные по ключам, относящихся к одному ISSN. (Тип dictionary):
   1. Общее количество ключей, относящихся к одному ISSN;
   2. Количеству успешно распознанных ключей, относящихся к одному ISSN;
   3. Количеству не успешно распознанных ключей, относящихся к одному ISSN;
   4. Количеству ключей, относящихся к одному ISSN, которые не были включены в возвращаемые данные по ISSN;  


### Установка библиотеки
Чтобы установить эту библиотеку, выполните следующую команду в терминале или командной консоли.  
```
> python -m pip install issn
```

### Как использовать библиотеку
Чтобы использовать эту библиотеку и получить данные публикации по ISSN, вам необходимо импортировать функцию `get_by_issn` 
из этого пакета и передать в нее ISSN.  

#### Пример:  
```
from issn.issn_api import get_by_issn

get_by_issn("2313-8246")
```
