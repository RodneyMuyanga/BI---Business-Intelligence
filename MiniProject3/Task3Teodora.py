import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

class EmployeeAttritionAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path

        # Load data
        try:
            self.df = pd.read_csv(self.data_path)
            st.success(f"Data loaded successfully from: {self.data_path}")
        except Exception as e:
            st.error(f"Failed to load data: {e}")
            raise

        # Map Attrition to binary and encode categorical variables
        self.df['Attrition'] = self.df['Attrition'].map({'Yes': 1, 'No': 0})
        self.df = pd.get_dummies(self.df, drop_first=True)

    def interpret_correlation(self):
        corr = self.df.corr()["Attrition"].sort_values(key=abs, ascending=False)
        strongest_feature = corr.index[1]  # index 0 is 'Attrition' itself
        strongest_corr = corr.iloc[1]

        if strongest_corr > 0:
            return f"The feature '{strongest_feature}' has the strongest positive correlation with attrition ({strongest_corr:.2f}), indicating employees with higher values in this feature are more likely to leave."
        else:
            return f"The feature '{strongest_feature}' has the strongest negative correlation with attrition ({strongest_corr:.2f}), indicating employees with higher values in this feature are less likely to leave."

    def interpret_confusion_matrix(self, cm):
        tn, fp, fn, tp = cm.ravel()
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        summary = (
            f"True Positives (correctly predicted attrition): {tp}\n"
            f"True Negatives (correctly predicted no attrition): {tn}\n"
            f"False Positives (incorrectly predicted attrition): {fp}\n"
            f"False Negatives (missed attrition cases): {fn}\n\n"
            f"Precision (of predicted attritions): {precision:.2f}\n"
            f"Recall (of actual attritions): {recall:.2f}\n"
        )
        return summary

    def interpret_decision_tree(self, clf, X):
        importances = clf.feature_importances_
        important_features = sorted(zip(X.columns, importances), key=lambda x: x[1], reverse=True)[:3]
        lines = ["Top 3 features used in the Decision Tree:"]
        for feat, imp in important_features:
            lines.append(f"- {feat} (importance: {imp:.3f})")
        return "\n".join(lines)

    def show_data_preview(self):
        st.write("### Data Preview")
        st.dataframe(self.df.head())

    def check_missing_values(self):
        st.write("### Missing Values")
        st.write(self.df.isnull().sum())

    def show_attrition_correlation(self):
        st.write("### Correlation with Attrition")
        corr = self.df.corr()["Attrition"].sort_values(key=abs, ascending=False)
        st.write(corr)

        interpretation = self.interpret_correlation()
        st.info(interpretation)

        fig, ax = plt.subplots(figsize=(10, 14))
        sns.barplot(x=corr.values, y=corr.index, ax=ax)
        ax.set_title("Features Sorted by Correlation with Attrition")
        ax.tick_params(axis='y', labelsize=10)
        st.pyplot(fig)

    def train_and_predict(self):
        X = self.df.drop('Attrition', axis=1)
        y = self.df['Attrition']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Decision Tree with class_weight balanced to handle imbalance
        clf = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42, class_weight='balanced')
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        st.write(f"### Accuracy: {accuracy * 100:.2f}%")

        st.write("### Classification Report")
        st.text(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        st.write("### Confusion Matrix")
        st.write(self.interpret_confusion_matrix(cm))

        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion Matrix")
        st.pyplot(fig)

        st.write("### Decision Tree Visualization")
        st.write(self.interpret_decision_tree(clf, X))

        fig, ax = plt.subplots(figsize=(20, 10))
        plot_tree(clf, filled=True, feature_names=X.columns, class_names=['No Attrition', 'Attrition'], ax=ax, rounded=True)
        st.pyplot(fig)

def main():
    st.title("Employee Attrition Analysis")

    data_path = 'WA_Fn-UseC_-HR-Employee-Attrition.csv'
    analysis = EmployeeAttritionAnalysis(data_path)

    st.sidebar.header("Select Analysis")
    choice = st.sidebar.radio("Choose one:", [
        "Data Preview",
        "Missing Values",
        "Correlation with Attrition",
        "Train and Predict"
    ])

    if choice == "Data Preview":
        analysis.show_data_preview()
    elif choice == "Missing Values":
        analysis.check_missing_values()
    elif choice == "Correlation with Attrition":
        analysis.show_attrition_correlation()
    elif choice == "Train and Predict":
        analysis.train_and_predict()

if __name__ == "__main__":
    main()
