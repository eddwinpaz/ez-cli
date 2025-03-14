## EZ Make

this script helps you generate a CRUD system for your project keeping it simple and compliant,
with internal coding style standards

## Features

- Generates a controller, service, repository and routes
- Generates a test for each of the above
- Appends new modules to Program.cs
- Easy to use command line interface
- JSON schema for entity definiton [Entity.json to Entity.cs]
- Pick your output folder
- Add Class Prefix and subfix names
- C# Net Core 

## Roadmap

- Nestjs (soon)
- Express (soon)
- Nano Framework (soon)

## Create virtual environment

```bash
python3 -m venv venv
```

## Run virtual environment

```bash
source venv/bin/activate
```

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 cli.py
```

## Entity example

```json
{
  "module": "Customer",
  "fields": [
    {
      "name": "FirstName",
      "type": "string",
      "size": 50
    },
    {
      "name": "LastName",
      "type": "string",
      "size": 50
    },
    {
      "name": "Email",
      "type": "string",
      "size": 100
    },
    {
      "name": "PhoneNumber",
      "type": "string",
      "size": 15
    },
    {
      "name": "DateOfBirth",
      "type": "DateTime"
    },
    {
      "name": "IsActive",
      "type": "bool"
    }
  ]
}

```

## Output

```bash
── output
│   ├── Customer
│   │   ├── Controllers
│   │   │   └── controller.cs
│   │   ├── Models
│   │   │   └── entity.cs
│   │   ├── Repositories
│   │   │   └── repository.cs
│   │   ├── Services
│   │   │   └── service.cs
│   │   └── Tests
│   │       ├── test_controller.cs
│   │       ├── test_entity.cs
│   │       ├── test_repository.cs
│   │       └── test_service.cs
│   └── Program.cs
```