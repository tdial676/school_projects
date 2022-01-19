package edu.caltech.cs2.project02.guessers;

import edu.caltech.cs2.project02.interfaces.IHangmanGuesser;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class AIHangmanGuesser implements IHangmanGuesser {
  private static String dictionary = "data/scrabble.txt";
  private static SortedSet<String> dict;

  @Override
  public char getGuess(String pattern, Set<Character> guesses) throws FileNotFoundException {
    Scanner scanner = new Scanner(new File(dictionary));
    dict = new TreeSet<>();
    while (scanner.hasNextLine()){
      String line = scanner.nextLine();
      this.dict.add(line);
    }
    scanner.close();
    SortedSet<String> subDict = new TreeSet<>();
    for (String word : dict) {
      if (findPattern(word, guesses).equals(pattern)) {
        subDict.add(word);
      }
    }
    Map<Character, Integer> rest = new TreeMap<>();
    String ALPHABET = "abcdefghijklmnopqrstuvwxyz";
    for (int i = 0; i < 26; i++) {
      if (guesses.contains(ALPHABET.charAt(i))){
        continue;
      }
      int j = 0;
      for (String word: subDict){
        if (word.indexOf(ALPHABET.charAt(i)) != -1) {
          j++;
        }
      }
      rest.put(ALPHABET.charAt(i), j);
    }
    char guess = '-';
    int k = 0;
    for (Character key: rest.keySet()) {
      if (k == 0) {
        guess = key;
        k++;
        continue;
      }
      if (rest.get(key) > rest.get(guess)) {
        guess = key;
      }
      k++;
    }
    return guess;
  }

  public  String findPattern(String word, Set<Character> guesses){
    String holder = "";
    for (int i = 0; i < word.length(); i++) {
      if (guesses.contains(word.charAt(i))) {
        holder += word.charAt(i);
      } else {
        holder += '-';
      }
    }
    return holder;
  }
}
