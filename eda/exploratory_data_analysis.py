# =========== libraries ===========
#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

#setting pandas options
pd.set_option('display.max_columns', None) #columns
pd.set_option('display.max_rows', 10)      #rows

# =========== paths and files ===========
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / 'data'
IMAGES_DIR = PROJECT_ROOT / 'images/eda'

df_housing = pd.read_csv(DATA_DIR / 'ames_housing.csv')

# =========== exploring data ===========
#basic information
#%%
df_housing.head()

#%%
print(df_housing.shape)

#%%
df_housing.describe()

#%%
#missing values
df_missing = pd.DataFrame({"column": df_housing.columns,
                           "missing_values": df_housing.isnull().sum().values,
                           "percentage": (df_housing.isnull().sum()/len(df_housing)*100).values})

df_missing = df_missing.query('missing_values>0').sort_values(by="missing_values", ascending=False).reset_index(drop=True)

#plotting missing values
plt.figure(figsize=(9, 5))

plt.bar(df_missing["column"], df_missing["missing_values"])
plt.title("Missing Values by Column", fontweight='bold')
plt.ylabel("Missing Values")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig(IMAGES_DIR / "missing_values.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
#target variable (Sale_Price) distribution
fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(df_housing['Sale_Price'], bins=50, edgecolor='black', alpha=0.7)
ax.set_title("Sale Price Distribution", fontweight='bold')
ax.set_xlabel("Sale Price")
ax.set_ylabel("Frequency")

plt.tight_layout()
plt.savefig(IMAGES_DIR / "target_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(df_housing['Lot_Area'], bins=50, edgecolor='black', alpha=0.7)
ax.set_title("Lot Area Distribution", fontweight='bold')
ax.set_xlabel("Lot Area")
ax.set_ylabel("Frequency")

plt.tight_layout()
plt.savefig(IMAGES_DIR / "lot_area_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
#checking if the sum of the areas is equal to the total area
print((df_housing['First_Flr_SF'].sum()+df_housing['Second_Flr_SF'].sum()+df_housing['Low_Qual_Fin_SF'].sum())-df_housing['Gr_Liv_Area'].sum())

#%%
#internal area price distribution
df_housing['internal_area'] = df_housing['Gr_Liv_Area'] + df_housing['Total_Bsmt_SF']
df_housing['internal_area_price'] = df_housing['Sale_Price'] / df_housing['internal_area']

fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(df_housing['internal_area_price'], bins=50, edgecolor='black', alpha=0.7)
ax.set_title("Internal Area Price Distribution", fontweight='bold')
ax.set_xlabel("Internal Area Price")
ax.set_ylabel("Frequency")

plt.tight_layout()
plt.savefig(IMAGES_DIR / "internal_area_price.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
#internal area distribution
fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(df_housing['internal_area'], bins=50, edgecolor='black', alpha=0.7)
ax.set_title("Internal Area Distribution", fontweight='bold')
ax.set_xlabel("Internal Area")
ax.set_ylabel("Frequency")

plt.tight_layout()
plt.savefig(IMAGES_DIR / "internal_area.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
#price per area and zone
fig, ax = plt.subplots(figsize=(10, 6))

sns.scatterplot(data=df_housing, x='internal_area_price', y='Sale_Price', hue='MS_Zoning', ax=ax)
ax.legend(bbox_to_anchor=(0.45, -0.22), loc='lower center', ncol=4)
ax.set_title("Price per Area and Zone", fontweight='bold')

plt.tight_layout()
plt.savefig(IMAGES_DIR / "price_per_area_zone.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
#correlation heatmap
correlation_cols = ['Lot_Frontage', 'Lot_Area', 'Mas_Vnr_Area', 'BsmtFin_SF_1', 'BsmtFin_SF_2', 'Bsmt_Unf_SF',
                    'Total_Bsmt_SF', 'First_Flr_SF', 'Second_Flr_SF', 'Low_Qual_Fin_SF', 'Gr_Liv_Area',
                    'Garage_Area', 'Wood_Deck_SF', 'Open_Porch_SF', 'Pool_Area', 'Sale_Price', 'internal_area']

corr = df_housing[correlation_cols].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0)
plt.title("Correlation Heatmap", fontweight='bold')
plt.savefig(IMAGES_DIR / "correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()

#%%
#neighbourhoods houses and prices
print(len(df_housing['Neighborhood'].unique()))

#houses per neighborhood
df_housing['Neighborhood'].value_counts()
sns.countplot(data=df_housing, y='Neighborhood', order=df_housing['Neighborhood'].value_counts().index)

plt.title("Houses per Neighborhood", fontweight='bold')
plt.savefig(IMAGES_DIR / "houses_per_neighborhood.png", dpi=300, bbox_inches="tight")
plt.show()

#price distribution per neighborhood
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_housing, x='Sale_Price', y='Neighborhood')
ax.set_title("Price Distribution per Neighborhood", fontweight='bold')
ax.set_ylabel(None)
plt.savefig(IMAGES_DIR / "price_distribution_per_neighborhood.png", dpi=300, bbox_inches="tight")
plt.show()