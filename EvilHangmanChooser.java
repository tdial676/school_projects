package edu.caltech.cs2.project02.choosers;

import edu.caltech.cs2.project02.interfaces.IHangmanChooser;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class EvilHangmanChooser implements IHangmanChooser {
  private static String dictionary = "data/scrabble.txt";
  private static final Random rand = new Random();
  private  int remainingGuesses;
  private SortedSet<Character> guesses;
  private SortedSet<String> family;
  private String pattern;

  public EvilHangmanChooser(int wordLength, int maxGuesses) throws FileNotFoundException {
    if (wordLength < 1 || maxGuesses < 1) {
      throw new IllegalArgumentException("Both Word length and max guesses must be greater than or equal to 1.");
    }
    Scanner scanner = new Scanner(new File(dictionary));
    String hold = null;
    this.family = new TreeSet<>();
    while (scanner.hasNextLine()) {
      hold = scanner.nextLine();
      if (hold.length() == wordLength) {
        family.add(hold);
      }
    }
    scanner.close();
    if (family.isEmpty()) {
      throw new IllegalStateException(" A word of the provided length, "+ wordLength + ", is out of range");
    }
    this.remainingGuesses = maxGuesses;
    this.guesses = new TreeSet<>();
    this.pattern = "";
    for (int i = 0; i < wordLength; i++) {
      this.pattern += '-';
    }
  }

  @Override
  public int makeGuess(char letter) {
    int count = 0;
    if (letter < 'a' || letter > 'z') {
      throw new IllegalArgumentException("The guessed letter must be in lowercase form.");
    }
    if (this.remainingGuesses < 1) {
      throw new IllegalStateException( "You have no more guesses left");
    }
    if (guesses.contains(letter)) {
      throw new IllegalArgumentException("You have already guessed the letter: " + letter);
    }
    this.guesses.add(letter);
    Map<String, SortedSet<String>> famTree = new TreeMap<>();
    for (String word : this.family) {
      String pattern = findPattern(word);
      if (!famTree.containsKey(pattern)) {
        famTree.put(pattern, new TreeSet<>());
      }
      famTree.get(pattern).add(word);
    }
    int i = 0;
    String topFam = "";
    for (String key: famTree.keySet()){
      if (i == 0) {
        topFam = key;
        i++;
        continue;
      }
      if (famTree.get(key).size() > famTree.get(topFam).size()) {
        topFam = key;
      } if (famTree.get(key).size() == famTree.get(topFam).size()) {
        if (key.compareTo(topFam) < 0) {
          topFam = key;
        }
      } i++;
    }
    this.pattern = topFam;
    this.family = famTree.get(this.pattern);
    String holder = topFam;
    for (int j = holder.indexOf(letter); j != -1; j = holder.indexOf(letter)) {
        count++;
        holder = holder.substring(j + 1);
    }
    if (count == 0) {
      this.remainingGuesses--;
    }
    return count;
  }

  @Override
  public boolean isGameOver() {
    int holder = 0;
    for (int i = 0; i < this.pattern.length(); i++) {
      if (this.pattern.charAt(i) == '-') {
        holder++;
      }
    }
    return (this.remainingGuesses < 1 || holder == 0);
  }

  @Override
  public String getPattern() {
    return this.pattern;
  }

  @Override
  public SortedSet<Character> getGuesses() {
    return this.guesses;
  }

  @Override
  public int getGuessesRemaining() {
    return this.remainingGuesses;
  }

  @Override
  public String getWord() {
    this.remainingGuesses = 0;
    int rdx = rand.nextInt(family.size());
    int i = 0;
    for (String word : family){
      if (i == rdx){
        return word;
      }
    }
    return null;
  }
  public  String findPattern(String word){
    String holder = "";
    for (int i = 0; i < word.length(); i++) {
      if (this.guesses.contains(word.charAt(i))) {
        holder += word.charAt(i);
      } else {
        holder += '-';
      }
    }
    return holder;
  }
}