# Katana ML Skipper Model Training Service

## Author

Katana ML, Andrej Baranovskij

## Instructions

1. Install libraries

```
pip install -r requirements.txt
```

2. Start service

```
python main.py
```

## Structure

```
.
├── app 
│   ├── queue
│       ├── event_producer.py
│       └── event_receiver.py
│   └── training_service.py
├── main.py
├── README.md
└── requirements.txt
```

## License

Licensed under the Apache License, Version 2.0. Copyright 2020-2021 Katana ML, Andrej Baranovskij. [Copy of the license](https://github.com/katanaml/katana-pipeline/blob/master/LICENSE).
