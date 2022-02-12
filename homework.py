class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить информационное сообщение"""
        return (f'Тип тренировки: {self.training_type};' 
                 f' Длительность: {self.duration:.3f} ч.;'
                 f' Дистанция: {self.distance:.3f} км;'
                 f' Ср. скорость: {self.speed:.3f} км/ч;'
                 f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    M_IN_KM = 1000
    LEN_STEP = 0.65


    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )    


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время бега"""
        COEFF_MINS = 60
        COEFF_CALORIE_1 = 18
        COEFF_CALORIE_2 = 20
        calories = ((COEFF_CALORIE_1 * self.get_mean_speed()
                    - COEFF_CALORIE_2) * self.weight / self.M_IN_KM * self.duration * COEFF_MINS)
        return calories 


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
                
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время ходьбы"""
        COEFF_MINS = 60
        COEFF_CALORIE_5 = 0.035
        COEFF_CALORIE_6 = 0.029
        calories: float = ((COEFF_CALORIE_5 * self.weight
                            + (self.get_mean_speed() ** 2 //self.height)
                            * COEFF_CALORIE_6 * self.weight) * self.duration * COEFF_MINS)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,   
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    LEN_STEP = 1.38
    COEFF_CALORIE_3 = 1.1
    COEFF_CALORIE_4 = 2

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.COEFF_CALORIE_3)
                    * self.COEFF_CALORIE_4 * self.weight)
        return calories

    def get_mean_speed(self) -> float:
        speed = ((self.length_pool * self.count_pool
                    / self.M_IN_KM / self.duration))
        return speed

                 

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    view_training = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    Final = view_training[workout_type](*data)
    return Final                             


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

