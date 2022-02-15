from dataclasses import dataclass, asdict
from typing import Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type};'
               ' Длительность: {duration:.3f} ч.;'
               ' Дистанция: {distance:.3f} км;'
               ' Ср. скорость: {speed:.3f} км/ч;'
               ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить информационное сообщение"""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    COEFF_MINS: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

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

    COEFF_MINS = 60
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время бега"""
        return ((self.COEFF_CALORIE_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.COEFF_MINS)


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

    COEFF_MINS = 60
    COEFF_CALORIE_5 = 0.035
    COEFF_CALORIE_6 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время ходьбы"""
        return ((self.COEFF_CALORIE_5
                 * self.weight
                 + (self.get_mean_speed()
                    ** 2
                    // self.height)
                 * self.COEFF_CALORIE_6
                 * self.weight)
                * self.duration
                * self.COEFF_MINS)


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
        """Получить количество затраченных калорий во время плавания"""
        return ((self.get_mean_speed()
                 + self.COEFF_CALORIE_3)
                * self.COEFF_CALORIE_4
                * self.weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость"""
        return ((self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration))


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    DataDict = Union['Running', 'SportsWalking', 'Swimming']
    CustomDict = dict[str, DataDict]
    view_training: CustomDict = {'SWM': Swimming,
                                 'RUN': Running,
                                 'WLK': SportsWalking}
    try:
        training = view_training[workout_type]

    except Exception:
        print('Отсутствует такой тип тренировки')
    final: DataDict = training(*data)
    return final


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
