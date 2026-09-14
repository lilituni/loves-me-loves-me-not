import random
from flower import Flower
import matplotlib.pyplot as plt

def start_game():
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box') 
    
    my_flower = Flower(random.randint(5, 13))
    my_flower.draw()

    def on_click(event):
        if event.xdata is None or event.ydata is None:
            return
        point = [event.xdata, event.ydata]
        # If clicked on the center of the flower, do nothing.
        if my_flower.circle_path.contains_point(point):
            return
        print(f"Clicked at: {point}")
        # Check if the click is inside any of the petals.
        for artist in my_flower.petal_paths:
            inside, _ = artist.contains(event)
            # Remove the petal if clicked inside it.
            if inside:
                print("You hit a petal!")
                artist.remove()
                my_flower.petal_paths.remove(artist)
                fig.canvas.draw_idle()
            if not my_flower.petal_paths:
                if my_flower.num_petals % 2 == 0:
                    print("Loves you not")
                else:
                    print("Loves you")
                # End the game if all petals are removed.
                return
    
    plt.margins(0.05) 
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

if __name__ == "__main__":
        start_game()