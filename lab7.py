from abc import ABC, abstractmethod

class Training(ABC):
    """Базовый класс тренировки."""

    def __init__(self, action: int, duration: float, weight: float):
        """
        action: количество действий (шагов или гребков),
        duration: продолжительность тренировки в часах,
        weight: вес пользователя в килограммах.
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    @abstractmethod
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        pass

    @abstractmethod
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        pass

    @abstractmethod
    def get_spent_calories(self) -> float:
        """Получить количество израсходованных калорий."""
        pass

    def show_training_info(self) -> str:
        """Вернуть информационное сообщение о тренировке."""
        return (f'Тип тренировки: {self.__class__.__name__}; '
                f'Длительность: {self.duration:.3f} ч; '
                f'Дистанция: {self.get_distance():.3f} км; '
                f'Ср. скорость: {self.get_mean_speed():.3f} км/ч; '
                f'Потрачено ккал: {self.get_spent_calories():.3f}.')


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    LEN_STEP = 0.65  # длина шага в метрах

    def get_distance(self) -> float:
        """Расчёт дистанции для бега в км."""
        return self.action * self.LEN_STEP / 1000

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Расчёт калорий для бега."""
        mean_speed = self.get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    LEN_STEP = 0.65  # длина шага в метрах

    def __init__(self, action: int, duration: float, weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        """Расчёт дистанции для ходьбы в км."""
        return self.action * self.LEN_STEP / 1000

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Расчёт калорий для ходьбы."""
        mean_speed = self.get_mean_speed()
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + (mean_speed**2 / self.height)
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # длина гребка в метрах
    CALORIES_SWIM_MULTIPLIER = 1.1
    CALORIES_SWIM_SHIFT = 2

    def __init__(self, action: int, duration: float, weight: float, pool_length: float, pool_count: int):
        super().__init__(action, duration, weight)
        self.pool_length = pool_length
        self.pool_count = pool_count

    def get_distance(self) -> float:
        """Расчёт дистанции для плавания в км."""
        return self.action * self.LEN_STEP / 1000

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Расчёт калорий для плавания."""
        mean_speed = self.get_mean_speed()
        return ((mean_speed + self.CALORIES_SWIM_MULTIPLIER)
                * self.CALORIES_SWIM_SHIFT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков."""
    workout_types = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type in workout_types:
        return workout_types[workout_type](*data)
    else:
        raise ValueError('Неизвестный тип тренировки')


def main():
    """Главная функция."""
    packages = [
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('SWM', [720, 1, 80, 25, 40])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        print(training.show_training_info())


if __name__ == '__main__':
    main()

