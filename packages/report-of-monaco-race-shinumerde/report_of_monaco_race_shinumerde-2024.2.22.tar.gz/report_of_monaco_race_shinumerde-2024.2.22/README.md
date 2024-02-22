#  Report of Monaco 2018 Racing

Report is a command-line tool that show statistic of race.

### Usage

To use Report, follow the instructions below:

### Installation

- Download package from _**PyPi**_ by following command:

```pip install report_of_monaco_race_shinumerde==2024.2.22```

> Make sure you have Python installed on your machine.

### Running the Application:

- Navigate to the **app** directory:

```cd app```

- Run the application using the following command:

```python report.py --file "data folder"```

```python report.py --file <race_data> --asc```

for ascendant sort or

```python report.py --file <race_data> --desc```

for descendant sort

Also you can see statistic for the driver by the command below

```python report.py --file <race_data> --driver "name of driver"```

### Example

```python report.py --file race_data "Lance Stroll"```

This will output:
```
 Lance Stroll │ WILLIAMS MERCEDES │ 1:13.323 
```
There are name of driver, car team and final time of race.

### License
>This project is licensed under the GNU Public License - see the LICENSE file for details.