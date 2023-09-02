class Data:
    class ProjectInfo:
        '''
        Описание свойств проекта
        '''

        Company = ""                #Компания
        Field = ""                  #Месторождение
        Well = ""                   #Скважина
        Bush = ""                   #Куст
        Engineer = ""               #Инженер по подбору
        ContactEngineer = ""        #Контакт инженера
        Date = ""                   #Дата подбора
        DateFormationPrice = ""     #Дата формирования цены
        TotalLength = 0             #Общая длина компоновки
        TotalCost = 0               #Общая стоимость реализации

    class HoleInfo:
        '''
        Описание свойств скважины
        '''

        WellBottomProjMD = 0        #Забой скважины (Проект MD)
        WellBottomProjTVD = 0       #Забой (Проект TVD)
        WellBottomFactTVD = 0       #Забой (Факт MD)
        WellBottomFactMD = 0        #Забой (Факт TVD)
        OpenHoleDiameter = 0        #Диаметр открыт ствола
        OffsetVertical = 0          #Смещение по вертикали
        OpenHoleLenght = 0          #Длина необсаж ствола
        MaxAngle = 0                #Макс зенитный угол
        MaxAngleInterval = 0        #Интервал макс зенит угла
        HoleType = ""               #Тип скважины
        ReservoirPressure = 0       #Пластовое давление
        WellheadPressure = 0        #Устьевое давление
        LinerRunningInterval = ""   #Интервал спуска хвостовиков
        NumberOfStagesGRP = 0       #Колво стадий ГРП
        DiameterExternal = 0        #Диаметр внешний
        DiameterInterior = 0        #Диаметр внутренний
        DescentDepth = 0            #Глубина спуска
        CKODdepth = 0               #Глубина ЦКОД
        CompositionType = ""        #Тип компоновки
