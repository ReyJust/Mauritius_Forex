# Mauritius Forex

Instantly get Forex rate of any bank of Mauritius in JSON! All that scraping is done for you. You just need to request urls.
Updates every 2 hour from 6am to 18pm on buisness days.

# Usage

## Get all forex

```sh
curl https://raw.githubusercontent.com/ReyJust/MCB_Forex/main/data/all.json
```

## Get all forex for a single bank

```sh
curl https://raw.githubusercontent.com/ReyJust/MCB_Forex/main/data/{bank_initial}/all.json
```

To view a list of `bank_initials`, please view the [Bank mapping](#bank-mapping). Note that all banks forex might not be available.

## Get a country forex for a single bank

```sh
curl https://raw.githubusercontent.com/ReyJust/MCB_Forex/main/data/{bank_initial}/{country_name}.json
```

To view a list of `country_name`, please view the [Country list](#country-list). That list is subject to changes. It depends on the BOM website content.

# Bank Mapping

| Bank Name                                  | Bank Initial  |
| ------------------------------------------ | ------------- |
| ABC Banking Corporation Ltd                | abc           |
| Absa Bank (Mauritius) Ltd                  | absa          |
| Afrasia Bank Limited                       | afbl          |
| Bank of Baroda                             | bob           |
| Bank of China                              | boc           |
| Bank One Limited                           | bol           |
| BCP Bank (Mauritius) Ltd                   | bcpbm         |
| British American Exchange Co. Ltd          | bae           |
| Century Banking Corporation Ltd            | cbcl          |
| Change Express Ltd                         | changeexpress |
| Habib Bank Limited                         | habib         |
| Hong Kong and Shanghai Banking Corporation | hsbc          |
| MauBank Ltd                                | maubank       |
| Mauritius Post Foreign Exchange Co Ltd     | mpfec         |
| Banque Patronus Limitée                    | patronus      |
| SBI (Mauritius) Ltd                        | sbim          |
| Shibani Finance                            | shib          |
| Standard Bank (Mauritius) Limited          | sbl           |
| State Bank of Mauritius                    | sbm           |
| Swan Forex Ltd                             | swan          |
| The Mauritius Commercial Bank Limited      | mcb           |
| Thomas Cook                                | tcook         |

# Country List

| Countries    |
| ------------ |
| australia    |
| canada       |
| china        |
| denmark      |
| emu          |
| hong_kong    |
| india        |
| japan        |
| new_zealand  |
| norway       |
| saudi_arabia |
| singapore    |
| south_africa |
| sweden       |
| switzerland  |
| ua_emirates  |
| uk           |
| usa          |

# DISCLAIMER

Banks and Forex Dealers submit to the Bank on business days the indicative exchange rates of the MUR against foreign currencies at which they would be willing to conduct retail transactions. Different rates apply to TT (electronic transfers), DD (bank drafts) and Notes. The Bank publishes the indicative exchange rates of banks and Forex Dealers on its website for public information, without any liability whatsoever.

I do not posses the data and I am not responsible of it's content.
