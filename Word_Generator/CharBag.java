import java.util.Random;

public class CharBag {
    private int[] charBag;
    private int size = 0;

    /*
     * Constructor of the char bag which sets the charBag array to be an integer
     * array of size 27. 1-26 for the alphabet and one more for '.'
     */
    public CharBag() {
        this.charBag = new int[27];

    }

    /*
     * Function that takes a char input and adds it to the appropriate alphabet
     * location in the charBag.
     */
    public void add(char input) {

        if (Character.isUpperCase(input)) {
            input = Character.toLowerCase(input);
        }

        int addIndex = removeHelper(input);
        if (addIndex == -1) {
            this.size++;
            this.charBag[26]++;
            return;
        }

        this.size++;
        this.charBag[addIndex]++;

    }

    /*
     * Function that takes an inputted char and returns how many occurences of that
     * char exist in the charBag.
     */
    public int getCount(char input) {
        if (Character.isUpperCase(input)) {
            input = Character.toLowerCase(input);
        }
        int index = removeHelper(input);
        if (index == -1) {
            return this.charBag[26];
        } else {
            return this.charBag[index];
        }

    }

    /*
     * Helper Function that which converts an inputted char into its integer
     * counterpart a-z would be 1-26. This integer will result in the index that the
     * char is at in the charBag
     */
    public int removeHelper(char input) {
        int index = 0;
        if (input < 'a' || input > 'z') {
            if (input == '.') {
                return 26;
            }
            return -1;
        }

        else {
            index = (int) (input - 'a');
        }

        return index;
    }

    /*
     * Remove which removes 1 occurence of the inputted char from the charBag. This
     * is done by first finding the index using the helper then decrementing the
     * value
     * present at charBag[index]
     */
    public void remove(char input) {
        if (Character.isUpperCase(input)) {
            input = Character.toLowerCase(input);
        }

        if (size == 0) {
            return;
        }

        int removeIndex = removeHelper(input);
        if (removeIndex == -1) {
            this.size--;
            this.charBag[26]--;
            return;
        }

        if (charBag[removeIndex] > 0) {
            this.size--;
            this.charBag[removeIndex]--;
        }
    }

    /* Get size function which returns the size of the charBag */
    public int getSize() {
        return this.size;
    }

    /*
     * A toString function which prints the charBag with all letters and their
     * counts in an appropriate format
     */
    public String toString() {
        String bagString = "CharBag{";
        int currentCount = 0;
        for (char c = 'a'; c <= 'z'; c++) {
            currentCount = getCount(c);
            bagString = bagString + c + ":" + currentCount + ", ";

        }
        int periodCount = getCount('.');
        bagString += '.' + ":" + periodCount + "}";
        return bagString;
    }

    /*
     * Function that returns a random char from the char bag based on how many
     * occurences of that char are in the bag.
     */
    public char getRandomChar() {
        Random rng = new Random();
        char ret = ' ';
        if (size > 0) {
            int count = rng.nextInt(size);
            for (char c = 'a'; c < 'z'; c++) {
                count -= getCount(c);
                if (count < 0) {
                    ret = c;
                    break;
                }
            }
        }

        if (Character.isLetter(ret)) {
            return ret;
        } else {
            return '.';
        }
    }
}