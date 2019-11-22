# fiautopilot

This project seeks to automate Financial Independence tasks.

## Configuration Files

The two config files below must be included, or the program will error.  Example config files are
included.

### General Config

You must include a `generalconfig.json` file with the following format, where:

* principal_stock - the amount of your current principal in today's dollars
* principal_inflation - your retirement goal amount in today's dollars
* rate_stock - projected rate of return
* rate_inflation - projected inflation rate
* number_of_compounds_per_year - the number of times principal compounds per year
* annual_contribution - the amount of your annual contribution

```
{
  "principal_stock": 0,
  "principal_inflation": 750000,
  "rate_stock": 0.08,
  "rate_inflation": 0.03,
  "number_of_compounds_per_year": 12,
  "annual_contribution": 7500
}
```

### Principal Stock History

You must include a `principalstockhistory.json` file with the following format, where:

* date - the date at which the stock value was taken
* principal_stock - the amount of the principal on the above date

```
{
  "principal_stock_history": [
    {
      "date": "201707",
      "principal_stock": 135000.00
    },
    {
      "date": "201710",
      "principal_stock": 140000.00
    }
  ]
}
```
