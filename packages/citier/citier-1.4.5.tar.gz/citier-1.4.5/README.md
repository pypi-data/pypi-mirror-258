# citier

Python Library to Validate and List Countires, States and cities.




## Installation

```bash
pip install citier
```



# Usage

<!-- Countries Start -->
## Country
```bash
from citier.country import validate_country, countries_list
```
### Validate any Country

```bash
validate_country("Pakistan")
```

### List a Range of countries
```bash
countries_list(1,2) 
```

### List all Countries
```bash
countries_list()
```




<!-- States Start -->
## State

```bash
from citier.state import validate_state, list_states
```

### Validate a State
```bash
validate_state("Punjab")
```

### List All States of a Country
```bash
list_states("Pakistan")
```




<!-- Cities Start -->
## City
```bash
from citier.city import list_cities, list_state_cities
```

### List All Cities of a Country
```bash
list_cities("Pakistan")
```

### List All Cities of a State
```bash
list_state_cities("Punjab")
```

