## Функция “issn_api”
В `issn_api` используеться функция `get_by_issn`, которая анализирует данные по ISSN.

### **Параметры**:
- issn - Идентификатор ISSN;

### **Возвращает**:
- Словарь “result” с данными по ISSN;


### **Список парсеров**:
- parse_issn_data;
- parse_issn_resource;
- parse_oraganization;
- parse_oraganization;
- parse_country_code;
- parse_status;
- parse_format;
- parse_key_title;
- parse_issn;
- parse_issnL;
- parse_record;


### **Словарь “result” с данными по ISSN**: 
```
result = {'issn': issn, 
          'data': {}, 
          'parse_errors': {}, 
          'parse_warnings': {}, 
          'errors': [], 
          'statistic': {}} 
```
 

### **Описание данных, возвращаемых из парсера “parse_issn_data”**:
- Тип: Dictionary;
- Возвращает: Словарь с данными об издании (публикации);


1) **issn** - идентификатор ISSN. (Тип string);
2) **data** - информация об издании (публикации). (Тип dictionary); 
Описание данных издания: 

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

3) **parse_errors** - ошибки, которые были найдены в других парсерах. (Тип dictionary);
4) **parse_warnings** - предупреждения, которые были найдены в других парсерах. (Тип dictionary);
5) unparsed_keys** - список ключей, которые не были распознаны.(Тип list); 
6) **unsuccessful** - список ключей, которые были не успешно проанализированы. (Тип list); 
7) **unparsed_b** - список ключей, наподобие такого формата “_:b1”, которые были найдены в ISSN. (Тип list);
8) **errors** - критические ошибки, которые могли возникнуть в таких случаях, как (Тип list):
   1. Отсутствие подключения интернета;
   2. Некорректный запрос на получение данных из сети;
   3. Некорректный формат данных, полученных из сети;

9) **statistic** - данные статистики по. (Тип dictionary):
   1. Количеству проанализированых ISSN;
   2. Количеству успешно проанализированых ключей, относящихся к одному ISSN;
   3. Количеству не успешно проанализированых ключей, относящихся к одному ISSN;
   4. Количеству коючей, относящихся к одному ISSN, которые  не были распознаны;

