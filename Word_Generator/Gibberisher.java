import java.util.Arrays;

public class Gibberisher {
    private Trie<CharBag> trieBag;
    private int segLength;
    private int size = 0;

    /*
     * Constructor which creates a new trie with data type of CharBag, the size to
     * 0, and the segment length to the input
     */

    public Gibberisher(int segLength) {
        trieBag = new Trie<CharBag>();
        this.size = size;
        this.segLength = segLength;
    }

    /*
     * Train function which takes a string array and trains the computer to
     * understand what letters came after what words. It does this by using the
     * lettersample to create segments of each word in the array. Each of these
     * segments is added into the Trie with a charbag containing the next letter.
     * With this we will a have a trie full of String segments and charbags. The
     * charbags will train the computer to know what letter comes after the
     * appropriate string
     */
    public void train(String[] strArr) {
        for (int i = 0; i < strArr.length; i++) {
            LetterSample[] newSamp = LetterSample.toSamples(strArr[i], segLength);
            for (int j = 0; j < newSamp.length; j++) {
                String segment = newSamp[j].getSegment();
                CharBag newBag = trieBag.get(segment);
                this.size++;
                if (newBag != null) {
                    char nextChar = newSamp[j].getNextLetter();
                    if (Character.isLetter(nextChar) || nextChar == '.') {
                        newBag.add(nextChar);
                        trieBag.put(segment, newBag);
                    }
                } else {
                    newBag = new CharBag();
                    char nextChar = newSamp[j].getNextLetter();
                    if (Character.isLetter(nextChar) || nextChar == '.') {
                        newBag.add(nextChar);
                        trieBag.put(segment, newBag);
                    }
                }
            }
        }
    }

    /*
     * Get sample count will return the number of samples in the trie or rather just
     * how many nodes are in the trie.
     */
    public int getSampleCount() {
        return this.size;
    }

    /*
     * Generate function which generates a random string word based on what is in
     * the Trie. It will choose a letters based on the train function before which
     * populates the trieBag. The trieBag contains all the possible string segments
     * and next letters. This using this we can create random words based on the
     * current word and all its letter segments.
     */

    public String generate() {
        String generateWord = "";
        String sample = "";

        char addchar = 'a';
        CharBag bag = new CharBag();
        int index = 1;
        boolean loop = true;

        while (loop) {
            if (addchar == '.') {
                loop = false;
            }

            if (generateWord.length() < segLength) {
                sample = generateWord;
                bag = trieBag.get(sample);
                addchar = bag.getRandomChar();
            } else if (generateWord.length() == segLength) {
                bag = trieBag.get(generateWord);
                if (bag != null) {
                    addchar = bag.getRandomChar();
                }
            } else {
                sample = generateWord.substring(index, segLength + index);
                bag = trieBag.get(sample);
                if (bag != null) {
                    addchar = bag.getRandomChar();
                    index++;
                }
            }

            generateWord += addchar;
        }

        generateWord = generateWord.replace(".", "");
        return generateWord;

    }
}
