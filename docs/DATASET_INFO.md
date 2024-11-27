### About Dataset:
This dataset and info was gathered from [kaggle](**https://www.kaggle.com/datasets/shudhanshusingh/250k-medicines-usage-side-effects-and-substitutes**)

This dataset contains comprehensive information on over 248,000 medical drugs from all manufacturers available worldwide. The data includes details such as drug names, active ingredients, therapeutic uses, dosage, side effects, and substitutes. The dataset aims to provide a useful resource for medical researchers, healthcare professionals, and drug manufacturers.

The dataset contains the following information for each drug:

* Drug name
* Adverse reactions and side effects
* Drug interactions
* Drug class
* Substitute drugs
* Active ingredients: Available in previous dataset published [here](https://www.kaggle.com/datasets/shudhanshusingh/az-medicine-dataset-of-india).

---

#### Dataset Related Info:

1. There are total of 5 substitute columns in the dataset.

2. There are total of 41 Side Effects columns in the dataset. Drugs with less side effects have those columns as NaN.

3. There are total of 5 usage columns in the dataset.

4. Rest Columns have their own individual identity.


`Substitute`: Indicates that whatever the name of the medicine, if the consumer want's to know alternative medicications that have the same composition, but manufactured by different companies. So 5 substitutes have been provided for each drug/medicine.

`Therapeutic Class`: It is a way of classifying medical drugs according to their functions. Each therapeutic class is a group of similar medications classified together because they are intended to treat the same medical conditions. (eg: Respiratory is one of the classes, so all medications treating this illness come under the same class.)

`Action Class`: A way of classifying medications based on actions they perform such as "H2 Receptor Blocker". It Block H2 receptors in parietal cells of the stomach, decreasing gastric acid secretion. So drugs with similar action are grouped under "H2 Receptor Blocker".

`Chemical Class`: As the name suggests, it is grouping based on chemical compound used.

`Habit Forming`: Classified as YES or NO. It is defined as the process of forming a habit, referring generally to psychological dependence on the continued use of a drug to maintain a sense of well-being, which can result in drug addiction. If there is a chance of drug addiction, then it is set to YES, otherwise NO.