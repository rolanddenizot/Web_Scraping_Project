from flask import Flask, render_template, redirect, request
import pandas as pd
import matplotlib.pyplot as plt
CUSTOM_PALETTE = ['#000000','#FF0000', '#008000', '#0000FF', '#800080', '#FFC300', '#800000', '#808080', '#00FF00', '#FF00FF']

app = Flask(__name__)

df_glob = pd.read_csv("input_files/input_file.csv")

classes = "table table-striped table-bordered"

lim = 1000

@app.route('/', methods=['GET', 'POST'])
def home():
    global lim
    lim = request.args.get("lim")
    lim = request.args.get("lim")
    lim = 1000 if lim is None else int(lim)
    return render_template('base.html')

@app.route('/requete0', methods=("POST", "GET"))
def requete0():
    df = df_glob.head(lim)
    return render_template('df_display.html', requete_name="See data",  result=df.to_html(classes="table table-striped table-bordered", index=False))

@app.route('/requete1', methods=("POST", "GET"))
def requete1():
    fig_name = "nb_products_by_brand"
    fig_path = f"static/images/{fig_name}.png"
    fig = plt.figure()
    df_glob.groupby("Marque").count()["Nom_produit"].sort_values().plot(kind="barh", figsize=(10, 5), color="black")
    plt.title("Number of products by brand", fontsize="xx-large")
    plt.xlabel("Number of products")
    plt.ylabel("Brand")
    plt.savefig(fig_path)
    plt.close(fig)
    return render_template('simple.html', requete_name="Number of products by brand", result=fig_path)

@app.route('/requete2', methods=("POST", "GET"))
def requete2():
    fig_name = "nb_products_by_gpu"
    fig_path = f"static/images/{fig_name}.png"
    fig = plt.figure()
    df_glob.groupby("Type du GPU").count()["Nom_produit"].sort_values().plot(kind="barh", figsize=(10, 5), color="purple")
    plt.title("Number of products by type of GPU", fontsize="xx-large")
    plt.xlabel("Number of products")
    plt.ylabel("Brand")
    plt.savefig(fig_path)
    plt.close(fig)
    return render_template('simple.html', requete_name="Number of products by type of GPU", result=fig_path)

@app.route('/requete3', methods=("POST", "GET"))
def requete3():
    fig_name = "nb_products_by_memory"
    fig_path = f"static/images/{fig_name}.png"
    fig = plt.figure()
    df_glob.groupby("Quantité Mémoire (Go)").count()["Nom_produit"].plot(kind="barh", figsize=(10, 5), color="red")
    plt.title("Number of products by Memory Quantity", fontsize="xx-large")
    plt.xlabel("Number of products")
    plt.ylabel("Brand")
    plt.savefig(fig_path)
    plt.close(fig)
    return render_template('simple.html', requete_name="Number of products by Memory Quantity", result=fig_path)

@app.route('/requete4', methods=("POST", "GET"))
def requete4():
    fig_name = "nb_products_by_chipset"
    fig_path = f"static/images/{fig_name}.png"
    fig = plt.figure()
    df_glob.groupby("Chipset Graphique").count()["Nom_produit"].plot(kind="barh", figsize=(10, 5), color="green")
    plt.title("Number of products by Graphical Chipset", fontsize="xx-large")
    plt.xlabel("Number of products")
    plt.ylabel("Graphical Chipset")
    plt.savefig(fig_path)
    plt.close(fig)
    return render_template('simple.html', requete_name="Number of products by Graphical Chipset", result=fig_path)

@app.route('/requete5', methods=("POST", "GET"))
def requete5():
    fig_name = "mean_price_by_chipset_bar"
    fig_path = f"static/images/{fig_name}.png"
    fig = plt.figure()
    df_glob.groupby("Chipset Graphique")["Prix (€)"].mean().plot(kind="barh", figsize=(10, 5), color="blue")
    plt.title("Mean price by Graphical Chipset", fontsize="xx-large")
    plt.xlabel("Mean Price")
    plt.ylabel("Graphical Chipset")
    plt.savefig(fig_path)
    plt.close(fig)
    return render_template('simple.html', requete_name="Mean price by Graphical Chipset", result=fig_path)

@app.route('/requete6', methods=("POST", "GET"))
def requete6():
    fig_name = "boxplot_price_by_chipset"
    fig_path = f"static/images/{fig_name}.png"
    fig, ax = plt.subplots(figsize=(12,6))
    df_glob.boxplot(column=['Prix (€)'], by=["Chipset Graphique"], ax=ax)
    plt.setp(ax.get_xticklabels(), **{"rotation": 45})
    plt.title("Boxplot of price by graphical chipset", fontsize="xx-large")
    plt.xlabel("Graphical Chipset")
    plt.ylabel("Price")
    plt.savefig(fig_path)
    plt.close(fig)
    return render_template('simple.html', requete_name="Boxplot of price by graphical chipset", result=fig_path)

@app.route('/requete7', methods=("POST", "GET"))
def requete7():
    fig_name = "price_in_function_of_memory_tech"
    fig_path = f"static/images/{fig_name}.png"
    fig, ax = plt.subplots(figsize=(12, 6))
    legend, count = [], 0
    for i, gp in df_glob.groupby("Type du GPU"):
        gp.groupby("Quantité Mémoire (Go)")[["Prix (€)"]].mean().plot(ax=ax, color=CUSTOM_PALETTE[count])
        count += 1
        legend.append(i)
    plt.setp(ax.get_xticklabels(), **{"rotation": 45})
    plt.grid()
    plt.legend(legend)
    plt.title("Price in function of the memory quantity", fontsize="xx-large")
    plt.xlabel("Memory Quantity")
    plt.ylabel("Price")
    plt.savefig(fig_path)
    plt.close(fig)
    return render_template('simple.html', requete_name="Price in function of the memory quantity", result=fig_path)

if __name__ == "__main__":
    app.run(debug=True)