import matplotlib.pyplot as plt
from gaia_cmd_plotter import _config


class GaiaCMDAxis(plt.Axes):
    """
    A matplotlib.pyplot.Axes object that displays a Gaia CMD background.
    Inherits from matplotlib.pyplot.Axes.
    """
    _background_image = plt.imread(_config.DATA_DIR / "gaia_cmd_background.png")
    _left, _right = -1.5, 5.4
    _bottom, _top = 19.0, -5.0
    _extent = (_left, _right, _bottom, _top)
    _aspec_ratio = (_right - _left) / abs(_top - _bottom)

    def __init__(self, fig, rect=None, **kwargs):
        """
        Constructor for GaiaCMDAxis.

        Parameters
        ----------
        fig : matplotlib.figure.Figure
        rect : list, optional
        kwargs : dict, optional
        """
        # Set default rect
        if rect is None:
            rect = [0.125, 0.110, 0.775, 0.770]

        # Set matplotlib style
        plt.style.use(_config.DATA_DIR / "gaia_cmd.mplstyle")

        # Call the parent class constructor
        super().__init__(fig, rect, **kwargs)

        # Set background image
        self.imshow(self._background_image, extent=self._extent, aspect=self._aspec_ratio)

        # Set axis labels
        self.set_xlabel(r"$\mathrm{G_{BP} - G_{RP}}$")
        self.set_ylabel(r"$\mathrm{M_G}$")

        fig.add_axes(self)


def main() -> None:
    fig = plt.figure(figsize=(8, 8))
    ax = GaiaCMDAxis(fig)
    # fig.add_axes(ax)
    ax.plot(2.3, 5.5, mfc="r", mec="k", marker="o", ms=7)
    plt.savefig(_config.TEST_DIR / "test_cmd.pdf")


if __name__ == "__main__":
    main()
