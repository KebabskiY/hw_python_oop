from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_M = 60

    action: str
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / (self.duration)

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Не определен метод в классе '
                                  f'{self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration * self.H_IN_M))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_CONST = 0.035
    WEIGHT_CONST_2 = 0.029
    KMH_IN_MS = 0.278
    SM_IN_M = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.WEIGHT_CONST * self.weight + ((self.get_mean_speed()
                * self.KMH_IN_MS)**2 / (self.height / self.SM_IN_M))
            * self.WEIGHT_CONST_2 * self.weight) * (self.duration
                                                    * self.H_IN_M))


class Swimming(Training):
    """Тренировка: плавание."""

    SWM_CONST_1 = 1.1
    SWM_CONST_2 = 2
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float, count_pool: int):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWM_CONST_1)
                * self.SWM_CONST_2 * self.weight
                * self.duration)


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_types: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking,
                                                }
    training: Training = workout_types[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""

    inform = training.show_training_info()
    print(inform.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
