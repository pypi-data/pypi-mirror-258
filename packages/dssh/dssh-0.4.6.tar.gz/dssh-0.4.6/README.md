# Connect Dev SSH

Simple and elegant python module that helps you to manage your ssh server based on environment. Like DEV, UAT, PRE-PROD, PROD etc.
You can customize your environments/servers config as per your requirements.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```
pip install dssh
```

## Usage

### Add new environment

```
dssh addenv
```

Output:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
└────────────────────────┘
New Environment name: DEV
```

### Delete an environment

```
dssh dlenv
```

Output:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
│ DEV                    │
└────────────────────────┘
Select an environment: DEV
```

### Add new server to an environment

```
dssh addserver
```

Output:

```
dssh addserver
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
│ DEV                    │
└────────────────────────┘
Select an environment: DEV
┏━━━━━━━━━━━━━━━━━━━┓
┃ Availbale Servers ┃
┡━━━━━━━━━━━━━━━━━━━┩
└───────────────────┘
New Server name: Server1
Server username: username
Server hostname: 10.10.0.1
Custom key path(path should be absolute)(Press enter if no change):
Does this server use bastion server y/n: n
```

### Connect to a server

```
dssh connect
```

Output:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
│ DEV                    │
│ UAT                    │
└────────────────────────┘
Select an environment: DEV
┏━━━━━━━━━━━━━━━━━━━┓
┃ Availbale Servers ┃
┡━━━━━━━━━━━━━━━━━━━┩
│ Server1           │
└───────────────────┘
Select a server: Server1
Environment:DEV Server:Server1!
Connecting to username@10.10.0.1! 💥
```

### Modify config of a server

```
dssh modserver
```

Output:

```
dssh modserver                    
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
│ DEV                    │
└────────────────────────┘
Select an environment: DEV
┏━━━━━━━━━━━━━━━━━━━┓
┃ Availbale Servers ┃
┡━━━━━━━━━━━━━━━━━━━┩
│ Server1           │
└───────────────────┘
Select a server: Server1
Current Username - username Hostname - 10.10.0.1
New Username(Press enter if no change): nusername
New Hostname(Press enter if no change): 10.10.0.2
New key path(path should be absolute)(Press enter if no change):
Do you want to update bastion server(y/n): n
Success! 💥
```

### Remove a server

```
dssh dlserver
```

Output:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Available Environments ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━┩
│ DEV                    │
└────────────────────────┘
Select an environment: DEV
┏━━━━━━━━━━━━━━━━━━━┓
┃ Availbale Servers ┃
┡━━━━━━━━━━━━━━━━━━━┩
│ Server1           │
└───────────────────┘
Select a server: Server1
Success! 💥
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
