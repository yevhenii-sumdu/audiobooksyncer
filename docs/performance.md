# Профілювання

## CPU

Для CPU профілювання я використав cProfile.

З результатів можна побачити, що найбільше часу займає синхронізація текстів, а саме виконання обчислень відеокартою.

Також досить багато часу займає синхронізація з аудіо.

Ще певний час займає траскрипція початку аудіофайлу (теж обчислення відеокартою).

## Memory

Для профілювання пам’яті я використав memory_profiler.

З результатів можна побачити, що після виклику функцій align_texts() та locate_chapters() використовується додаткова оперативна пам’ять, що може бути звільнена.

Також, такий самий результат можна побачити щодо використання відеопам’яті.
