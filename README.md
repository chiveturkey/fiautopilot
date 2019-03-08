# fiautopilot

This project seeks to automate Financial Independence tasks.

## Configuration File

If you would like to override, default system constants, include a config.json file with the following format, where:

* principal_stock - the amount of your current principal in today's dollars
* principal_inflation - your retirement goal amount in today's dollars
* rate_stock - projected rate of return
* rate_inflation - projected inflation rate
* number_of_compounds_per_year - the number of times principal compounds per year

```
{
  "principal_stock": 0,
  "principal_inflation": 750000,
  "rate_stock": 0.08,
  "rate_inflation": 0.03,
  "number_of_compounds_per_year": 12
}
```
