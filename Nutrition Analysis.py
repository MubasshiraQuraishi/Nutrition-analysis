#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


# In[2]:


data = pd.read_csv('C:\\Users\\Mubasshira\\Downloads\\nutrients_data.csv')
data.head(7)


# In[3]:


data.info()


# In[4]:


categorical_columns = data.select_dtypes('O').columns
data[categorical_columns].describe()


# In[5]:


data.info()


# # Statistical Analysis

# In[6]:


numerical_columns = data.select_dtypes(['float64','int64']).columns
data[numerical_columns].describe()


# In[7]:


summary_stats = data.groupby('Category').agg({
    'Calories':['mean','median'],
    'Protein':['mean','median'],
    'Fat':['mean','median'],
    'Sat. Fat':['mean','median'],
    'Fiber':['mean','median'],
    'Carbs':['mean','median'],
}).reset_index()

summary_stats


# In[8]:


data.head()


# # High Protein and Low Sat. Fat

# In[9]:


high_protein_low_satfat = data[(data['Protein'] > data['Protein'].quantile(0.75)) &
                               (data['Sat. Fat'] < data['Sat. Fat'].quantile(0.50)) &
                               (data['Fat'] < data['Fat'].quantile(0.75))]

high_protein_low_satfat.sort_values(by='Protein', ascending=False)


# In[10]:


data.columns


# # Food content Distribution 

# In[11]:


required_columns = ['Calories', 'Protein', 'Fat', 'Sat. Fat','Fiber', 'Carbs']
grouped_data = data.groupby('Category')[required_columns].sum()

fig, ax = plt.subplots(figsize=(10, 6))
grouped_data.plot(kind='bar', ax = ax, edgecolor='white', width = 0.6)

ax.set_xticklabels([str(q) for q in grouped_data.index], rotation=45, ha='right')
plt.xlabel('Category')
plt.ylabel('Amounts')
plt.title('Nutritional Components by Category')
plt.tight_layout()
plt.show()


# In[12]:


required_columns = ['Protein', 'Fat', 'Sat. Fat','Fiber', 'Carbs']
grouped_data = data.groupby('Category')[required_columns].sum()

fig, ax = plt.subplots(figsize=(14, 6))
grouped_data.plot(kind='bar', ax = ax, edgecolor='white', width = 0.8)

ax.set_xticklabels([str(q) for q in grouped_data.index], rotation=45, ha='right')
plt.xlabel('Category')
plt.ylabel('Amounts')
plt.title('Nutritional Components by Category')
plt.tight_layout()
plt.show()


# More-
# 
# 
# -- Fiber:
# Higher fiber content is generally beneficial for digestive health and can help with weight management and lowering the risk of chronic diseases.
# 
# -- Protein:
# Sufficient protein intake is essential for muscle repair, immune function, and overall health. It’s often considered good to have more protein in the diet, particularly for active individuals or those looking to build muscle.
# 
# -- Carbs: Carbohydrates are a primary source of energy. However, it's crucial to focus on the type of carbs (complex vs. simple) and their quantity, aiming for complex carbs (like whole grains) rather than simple sugars.
# 
# 
# Less-
# 
# 
# -- Fat: While fat is necessary for bodily functions, excessive intake can lead to health issues such as heart disease. It’s beneficial to limit total fat intake and focus on healthy fats.
# 
# -- Saturated Fat: Saturated fats, found in animal products and some processed foods, should be consumed in moderation as they can raise cholesterol levels and increase the risk of heart disease.
# 
# -- Calories: Managing calorie intake is crucial for maintaining a healthy weight. Consuming more calories than needed can lead to weight gain, while too few can lead to malnutrition. Balancing calorie intake according to your energy expenditure is key.

# # Correlation Analysis

# In[13]:


corr_data = data[['Calories', 'Protein', 'Fat', 'Sat. Fat', 'Fiber', 'Carbs']]
plt.figure(figsize=(9,5))
sns.heatmap(corr_data.corr(), annot = True, cmap = 'PiYG')


# High Correlations:
# 
# - Fat and Saturated Fat: Strongly related due to their nature.
# - Protein and Saturated Fat: Strongly related, especially in high-fat protein sources.
# - Fiber and Protein: High correlation due to the presence of fiber-rich protein sources.
#     
#     
# Moderate Correlations:
# 
# - Fiber and Fat: Moderate association due to high-fiber foods sometimes containing fats.
# - Fiber and Carbs: Moderate correlation as many high-fiber foods are also high in carbs.
# - Carbs and Protein: Moderate association as some foods contain both nutrients.

# # High Fat and High Saturated Fat Analysis

# In[14]:


highfat_and_highsatfat = data[(data['Fat'] > data['Fat'].quantile(0.80)) & 
                             (data['Sat. Fat'] > data['Sat. Fat'].quantile(0.80))]
highfat_and_highsatfat_sorted = highfat_and_highsatfat.sort_values(by='Fat', ascending=False)
highfat_and_highsatfat_top = highfat_and_highsatfat_sorted.groupby('Category').head(5)


# In[15]:


categories = highfat_and_highsatfat_top['Category'].unique()
n_rows = 2
n_cols = 4
fig, axes = plt.subplots(n_rows, n_cols,figsize=(20, 10))
axes = axes.flatten()
for ax, category in zip(axes, categories):
    category_data = highfat_and_highsatfat_top[highfat_and_highsatfat_top['Category'] == category]
    food_items = category_data['Food']
    fat_values = category_data['Fat']
    sat_fat_values = category_data['Sat. Fat']
    
    # Plot bars for Fat and Sat. Fat
    ax.bar(food_items, fat_values, width=0.4, label='Fat', align='center', color='indianred')
    ax.bar(food_items, sat_fat_values, width=0.4, label='Sat. Fat', align='edge',color='forestgreen')

    ax.set_ylabel('Amount')
    ax.set_title(f' High Fat and Saturated Fat in {category}')
    ax.legend()
    ax.set_xticklabels(food_items, rotation=45, ha='right')

plt.tight_layout()
plt.show()


# # Low Fat and Low Saturated Fat Analysis

# In[16]:


low_fat_low_satfat = data[(data['Fat'] < data['Fat'].quantile(0.75)) & 
                             (data['Sat. Fat'] < data['Sat. Fat'].quantile(0.75))]
low_fat_low_satfat_sorted = low_fat_low_satfat.sort_values(by='Fat', ascending=True)
low_fat_low_satfat_top = low_fat_low_satfat_sorted.groupby('Category').head(5)


# In[17]:


categories = low_fat_low_satfat_top['Category'].unique()
n_rows = 2
n_cols = 4
fig, axes = plt.subplots(n_rows, n_cols,figsize=(20, 10))
axes = axes.flatten()
for ax, category in zip(axes, categories):
    category_data = low_fat_low_satfat_top[low_fat_low_satfat_top['Category'] == category]
    food_items = category_data['Food']
    fat_values = category_data['Fat']
    sat_fat_values = category_data['Sat. Fat']
    
    ax.bar(food_items, fat_values, width=0.4, label='Fat', align='center', color='indianred')
    ax.bar(food_items, sat_fat_values, width=0.4, label='Sat. Fat', align='edge', color='forestgreen')

    ax.set_ylabel('Amount')
    ax.set_title(f' Low Fat and Saturated Fat in {category}')
    ax.legend()
    ax.set_xticklabels(food_items, rotation=45, ha='right')

plt.tight_layout()
plt.show()


# # High Protein and High Fat Analyis

# In[18]:


highprotein_and_highfat = data[(data['Protein'] > data['Protein'].quantile(0.80)) &
                              (data['Fat'] > data['Fat'].quantile(0.80))]
highprotein_and_highfat_sorted = highprotein_and_highfat.sort_values(by='Protein', ascending=False)
highprotein_and_highfat_top = highprotein_and_highfat_sorted.groupby('Category').head(5)


# In[19]:


categories = highprotein_and_highfat_top['Category'].unique()
n_rows = 2
n_cols = 3
fig, axes = plt.subplots(n_rows, n_cols,figsize=(20, 10))
axes = axes.flatten()
for ax, category in zip(axes, categories):
    category_data = highprotein_and_highfat_top[highprotein_and_highfat_top['Category'] == category]
    food_items = category_data['Food']
    fat_values = category_data['Fat']
    protein_values = category_data['Protein']
    
    ax.bar(food_items, fat_values, width=0.4, label='Fat', align='center',color='palevioletred')
    ax.bar(food_items, protein_values, width=0.4, label='Protein', align='edge',color = 'teal')

    ax.set_ylabel('Amount')
    ax.set_title(f'High Fat and Protein in {category}')
    ax.legend()
    ax.set_xticklabels(food_items, rotation=45, ha='right')

plt.tight_layout()
plt.show()


# # Low Protein and Low Fat Analyis

# In[20]:


lowprotein_and_lowfat = data[(data['Protein'] < data['Protein'].quantile(0.60)) &
                              (data['Fat'] < data['Fat'].quantile(0.60))]
lowprotein_and_lowfat_sorted = lowprotein_and_lowfat.sort_values(by='Protein', ascending=True)
lowprotein_and_lowfat_top = lowprotein_and_lowfat_sorted.groupby('Category').head(5)


# In[21]:


categories = lowprotein_and_lowfat_top['Category'].unique()
n_rows = 2
n_cols = 4
fig, axes = plt.subplots(n_rows, n_cols,figsize=(20, 10))
axes = axes.flatten()
for ax, category in zip(axes, categories):
    category_data = lowprotein_and_lowfat_top[lowprotein_and_lowfat_top['Category'] == category]
    food_items = category_data['Food']
    fat_values = category_data['Fat']
    protein_values = category_data['Protein']
    
    ax.bar(food_items, fat_values, width=0.4, label='Fat', align='center',color='palevioletred')
    ax.bar(food_items, protein_values, width=0.4, label='Protein', align='edge',color = 'teal')

    ax.set_ylabel('Amount')
    ax.set_title(f'Low Fat and Protein in {category}')
    ax.legend()
    ax.set_xticklabels(food_items, rotation=45, ha='right')

plt.tight_layout()
plt.show()


# # High Protein and High Fiber Analyis

# In[22]:


highprotein_and_highfiber = data[(data['Protein'] > data['Protein'].quantile(0.75)) &
                              (data['Fiber'] > data['Fiber'].quantile(0.75))]
highprotein_and_highfiber_sorted = highprotein_and_highfiber.sort_values(by='Protein', ascending=False)
highprotein_and_highfiber_top5 = highprotein_and_highfiber_sorted.groupby('Category').head(5)


# In[23]:


categories = highprotein_and_highfiber_top5['Category'].unique()
n_rows = 2
n_cols = 3
fig, axes = plt.subplots(n_rows, n_cols,figsize=(20, 10))
axes = axes.flatten()
for ax, category in zip(axes, categories):
    category_data = highprotein_and_highfiber_top5[highprotein_and_highfiber_top5['Category'] == category]
    food_items = category_data['Food']
    protein_values = category_data['Protein']
    fiber_values = category_data['Fiber']
    
    ax.bar(food_items, protein_values, width=0.4, label='Protein', align='center',color='palevioletred')
    ax.bar(food_items, fiber_values, width=0.4, label='Fiber', align='edge',color = 'mediumpurple')

    ax.set_ylabel('Amount')
    ax.set_title(f'Protein and Fiber in {category}')
    ax.legend()
    ax.set_xticklabels(food_items, rotation=45, ha='right')

plt.tight_layout()
plt.show()


# # Food Content distribution by Categories - A pie charts analysis

# In[24]:


required_columns = ['Calories','Protein', 'Fat', 'Sat. Fat','Fiber', 'Carbs']
grouped_data = data.groupby('Category')[required_columns].sum()

n_rows = 2
n_cols = 3
fig, axes = plt.subplots(n_rows, n_cols,figsize=(20, 10))
axes = axes.flatten()
for i, column in enumerate(required_columns):
    if i < len(axes):
        grouped_data[column].plot(kind='pie', ax=axes[i], autopct='%1.1f%%', startangle=90, legend=False)
        axes[i].set_title(f'{column} distribution by Category')
        axes[i].set_ylabel('')
        
plt.tight_layout()
plt.show()


# - Calories = More in Vegetables
# - Protein = Fish, seafood
# - Fat = fats, oils, shortenings
# - sat fat = fats, oils, shortenings
# - Fiber = Fish, Seafood
# - Carbs = Fruits

# In[25]:


grouped_data


# # Carbohydrates Analysis

# In[26]:


from PIL import Image
img  = Image.open('carbs.png')
img


# In[27]:


carb = data[data['Carbs'] > 80].sort_values(by='Carbs', ascending=True)
cmap = plt.get_cmap('RdPu')
colors = cmap(np.linspace(0, 1, len(carb['Food'])))
plt.figure(figsize=(12,5))
plt.barh(y=carb['Food'],width=carb['Carbs'], color=colors)
plt.xlabel("Food")
plt.ylabel("Amount of Carbs")
plt.title("Food items having High Carbs")
plt.xticks(rotation=90)
plt.show()


# - Simple Carbohydrates  are composed of one or two sugar molecules and are quickly digested and absorbed. They often cause rapid spikes in blood sugar levels.
# - Complex carbohydrates are made up of long chains of sugar molecules and take longer to digest. They provide a more gradual and sustained release of energy.

# ### Carbohydrate Classification
# 
# | Simple Carbohydrates           | Complex Carbohydrates      |
# |--------------------------------|----------------------------|
# | Cranberry sauce sweetened      | Rice                       |
# | Dates                          | Wheat (all-purpose)        |
# | Fortified milk                 | Whole-wheat                |
# | Lemonade                       |                            |
# | Prunes                         |                            |
# | Puddings Sugar                 |                            |
# | Raisins                        |                            |
# | Rhubarb sweetened              |                            |
# 

# # Nutritional Insights

# | **Category**                        | **Food Items**                               | **Nutritional Insights**                                                                                                      |
# |-------------------------------------|----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
# | **Meat and Poultry**                | - Beef<br>- Roasted Chicken                  | - Excellent sources of protein<br>- Relatively low in fats                                                                    |
# | **Fish and Seafood**                | - Oysters<br>- Shrimps<br>- Lobster<br>- Clams | - Oysters: High in protein, fiber, and fats (consume in moderation)<br>- Shrimps, Lobster, Clams: High in fiber and protein, low in fat |
# | **Vegetables**                      | - Soybeans<br>- Lentils<br>- Red Kidney Beans<br>- Radishes<br>- Cucumbers<br>- Rutabagas (Root Vegetable) | - Soybeans, Lentils, Red Kidney Beans: High in protein<br>- Radishes, Cucumbers, Rutabagas: No fats, great for weight management |
# | **Dairy Products**                  | - Milk<br>- Ice Cream<br>- Skim Milk<br>- Cheddar Cheese | - Milk: High in protein and fats<br>- Ice Cream: High in protein but also high in fats<br>- Skim Milk: Lower-fat alternative<br>- Cheddar Cheese: Low in fat and high in protein |
# | **Breads, Cereals, Fast Food, Grains** | - Rice<br>- Wheat (all-purpose)<br>- Wheat (whole)<br>- Corn Meal<br>- Oatmeal | - Rice, Wheat (all-purpose): High in carbohydrates (complex carbs, should be consumed in moderation)<br>- Wheat (whole), Corn Meal: Moderately high in carbs, better than all-purpose wheat<br>- Oatmeal: Low in carbs, high in fiber |
# | **Soups**                           | - Bouillon<br>- Vegetable Soup<br>- Chicken Soup | - Low in fats and high in protein                                                                                              |
# | **Seeds and Nuts**                  | - Almonds<br>- Sunflower Seeds<br>- Peanuts | - High in protein, fiber, and healthy fats                                                                                     |
# | **Fruits**                          | - Blackberries<br>- Dates<br>- Watermelons<br>- Cantaloupe | - Rich in fibers, essential for digestive health                                                                               |
# | **Fats, Oils, Shortenings**         | - Yolks<br>- Butter                          | - Yolks: Contains fats in acceptable amounts<br>- Butter: High in fats, saturated fats, protein, fiber, carbs, and calories (considered less healthy) |
# | **Desserts and Sweets**             | - Chocolate Syrup                            | - Contains no protein, fat, saturated fat, or fiber<br>- Moderately high in calories                                           |
# | **Jams and Jellies**                | - Molasses                                   | - The most appropriate food choice in this category                                                                           |
# 

# In[ ]:




