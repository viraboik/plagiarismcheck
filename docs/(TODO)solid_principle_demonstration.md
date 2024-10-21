## Principles
- **Single-responsibility principle: "There should never be more than one reason for a class to change."** \
In other words, every class should have only one responsibility.\
Нащадки класу ABCDatabase, відповідають лише за взаємодію з базою даних, що реалізовує цей принцип


- **Interface segregation principle: "Clients should not be forced to depend upon interfaces that they do not use."**\
Інтерфейси, який я надала, це єдиний інтерфейс, який їм потрібний.  


- **Dependency inversion principle: "Depend upon abstractions, not concretes."**\
Мій database обєкт, який використовується FastAPI є абстрактим класом ABCDatabase і моя програма не залежить від реалізації цього класу.\
На даний момент я використовую реалізацію InMemoryDatabase, але я можу замінити цю реалізацію на MySQLDatabase і це не порушить роботу мого веб-застосунку. 
