public class TrieNode<T> {
    private T data;
    private TrieNode<T>[] treeLinks = new TrieNode[26];

    /*
     * Constructor which sets data to null and sets all treelinks of the node to
     * null since no links are present.
     */
    public TrieNode() {
        this.data = null;
        for (int i = 0; i < treeLinks.length; i++) {
            this.treeLinks[i] = null;
        }
    }

    /* Getter which returns the data stored at accosciated node. */
    public T getData() {
        return this.data;
    }

    /* Setter which sets the data of the node based on the given input. */
    public void setData(T data) {
        this.data = data;
    }

    /*
     * The getchild function will retrive the child nodes accosciated with an
     * inputted char. It does this by searching the treelinks array at the
     * appropriate letter index (input char converted to int).
     */
    public TrieNode<T> getChild(char c) {
        int index = 0;
        if (c < 'a' || c > 'z') {
            return null;
        }

        else {
            index = (int) (c - 'a');
        }

        if (treeLinks[index] == null) {
            treeLinks[index] = new TrieNode<T>();
        }

        return treeLinks[index];

    }

}
