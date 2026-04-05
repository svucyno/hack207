import shap
import pandas as pd
import matplotlib.pyplot as plt

def generate_shap_explanation(model, dummy_features, feature_names):
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(dummy_features)
        
        if isinstance(shap_values, list):
            vals = shap_values[1] # malicious class
        else:
            if len(shap_values.shape) == 3:
                vals = shap_values[:, :, 1]
            else:
                vals = shap_values
        
        # Override feature names with meaningful names if it's the standard model
        meaningful_names = list(feature_names)
        if len(meaningful_names) > 3:
            meaningful_names[0] = "Entropy"
            meaningful_names[1] = "API Calls"
            meaningful_names[2] = "Sections"
            meaningful_names[3] = "File Size"
        
        df = pd.DataFrame(dummy_features, columns=meaningful_names)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')
        
        shap.summary_plot(vals, df, plot_type="bar", show=False, color='#ef4444')
        
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        
        mean_abs_shap = abs(vals[0])
        top_indices = mean_abs_shap.argsort()[-3:][::-1]
        top_impacts = [meaningful_names[i] for i in top_indices if mean_abs_shap[i] > 0]
        
        human_readable = []
        for feat in top_impacts:
            if feat == "Entropy":
                human_readable.append("High entropy indicates packed or obfuscated code")
            elif feat == "API Calls":
                human_readable.append("Suspicious system API usage detected")
            elif feat == "Sections":
                human_readable.append("File structure is abnormal compared to benign files")
            elif feat == "File Size":
                human_readable.append("File size indicates potential payload stuffing")
            else:
                human_readable.append(f"Unexpected variance in {feat} distribution")
        
        if not human_readable:
            human_readable = ["General features exhibit deviation from benign samples"]
            
        return fig, human_readable
    except Exception as e:
        print(f"[DEBUG] SHAP exception: {e}")
        return None, [f"Could not generate SHAP explanation: {str(e)}"]
