import glob
import os
from .theme import Theme
from typing import Union

def load_theme(theme_name: str):
    """
    Sets the chosen style and color palette globally.

    :param theme_name: name of the theme to load
    :return: the specified Theme
    :raise ValueError: if a theme is not found
    """
    themes = _get_themes()
    if theme_name in themes.keys():
        return Theme.from_file(themes[theme_name])
    else:
        raise ValueError(f"No theme named '{theme_name}' found. Available options are: {list(_get_themes().keys())}")


def list_themes():
    """
    Returns a list of available theme names.

    :return: a list of available theme names
    """
    return list(_get_themes().keys())


def _get_themes():
    """
    Returns available themes from the theme directory

    :return: a {name: path} dict of all available themes
    """
    loc = os.path.dirname(os.path.abspath(__file__))
    return dict(
        map(
            lambda x: (os.path.basename(x).split(".")[0], x),
            glob.glob(os.path.join(loc, "themes", "*.json")),
        )
    )

def _sample_plot(theme: Union[Theme, str], save_as: str = None):
    """
    Generates a sample plot for a given theme. Optionally saves it to the specified location.

    :param theme: Theme instance or theme name to load.
    :param save_as: path to save the generated plot to
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    if type(theme) == str:
        theme = load_theme(theme)

    with theme:
        geysers = (
            sns.load_dataset("geyser")
            .rename(
                columns={
                    "duration": "Duration",
                    "kind": "Kind",
                    "waiting": "Waiting",
                }
            )
            .replace({"long": "Long", "short": "Short"})
        )
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        # Hacky patched boxplot since seaborn overrides color options otherwise
        # sns.boxplot(x="Kind", y="Duration", data=tips, ax=ax[0])
        ax[0].boxplot(
            [
                geysers.loc[geysers["Kind"] == "Long", "Duration"].tolist(),
                geysers.loc[geysers["Kind"] == "Short", "Duration"].tolist(),
            ],
            vert=True,
            patch_artist=True,
            labels=geysers["Kind"].unique(),
        )
        sns.kdeplot(
            x="Waiting", y="Duration", hue="Kind", data=geysers, ax=ax[1], fill=True
        )
        sns.lineplot(x="Waiting", y="Duration", hue="Kind", data=geysers, ax=ax[2])
        plt.suptitle("Geysers")

        if save_as is not None:
            fig.savefig(
                save_as,
                dpi=75,
                transparent=False,
                facecolor=fig.get_facecolor(),
                bbox_inches="tight",
            )

def make_samples():
    """
    Generates sample plots for all themes to be used in documentation
    """
    for theme in list_themes():
        _sample_plot(theme, f"assets/{theme}.png")

