import type { Monaco } from '@monaco-editor/react';
import type * as monacoTypes from 'monaco-editor';

/* ------------------------------------------------------------------ */
/* Custom editor themes that match the app palette ("Ink & Amber").    */
/* ------------------------------------------------------------------ */

export function defineDsaThemes(monaco: Monaco): void {
  monaco.editor.defineTheme('dsa-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'keyword', foreground: 'f2a93b', fontStyle: 'bold' },
      { token: 'keyword.control', foreground: 'f2a93b', fontStyle: 'bold' },
      { token: 'string', foreground: '9ece9a' },
      { token: 'number', foreground: 'f78c6c' },
      { token: 'comment', foreground: '5d6776', fontStyle: 'italic' },
      { token: 'type', foreground: '7dd3fc' },
      { token: 'annotation', foreground: 'c792ea' },
    ],
    colors: {
      'editor.background': '#0d1117',
      'editor.foreground': '#e9edf4',
      'editor.lineHighlightBackground': '#141a2388',
      'editorCursor.foreground': '#f2a93b',
      'editor.selectionBackground': '#3d2f1655',
      'editor.inactiveSelectionBackground': '#3d2f1633',
      'editorLineNumber.foreground': '#4b5563',
      'editorLineNumber.activeForeground': '#9aa3b2',
      'editorWidget.background': '#141a23',
      'editorWidget.border': '#232c38',
      'editorSuggestWidget.selectedBackground': '#3d2f16',
      'editorSuggestWidget.highlightForeground': '#f2a93b',
      'editor.hoverHighlightBackground': '#3d2f1633',
      'editorIndentGuide.background1': '#232c38',
      'editorIndentGuide.activeBackground1': '#314052',
    },
  });

  monaco.editor.defineTheme('dsa-light', {
    base: 'vs',
    inherit: true,
    rules: [
      { token: 'keyword', foreground: 'b45f06', fontStyle: 'bold' },
      { token: 'keyword.control', foreground: 'b45f06', fontStyle: 'bold' },
      { token: 'string', foreground: '2d7d46' },
      { token: 'number', foreground: 'b3541e' },
      { token: 'comment', foreground: 'a2937c', fontStyle: 'italic' },
      { token: 'type', foreground: '0284c7' },
      { token: 'annotation', foreground: '7c3aed' },
    ],
    colors: {
      'editor.background': '#faf7f1',
      'editor.foreground': '#211c14',
      'editor.lineHighlightBackground': '#f0eadd88',
      'editorCursor.foreground': '#b45f06',
      'editor.selectionBackground': '#f2d9a855',
      'editorLineNumber.foreground': '#a2937c',
      'editorLineNumber.activeForeground': '#6f6455',
      'editorWidget.background': '#ffffff',
      'editorWidget.border': '#e4dac6',
      'editorSuggestWidget.selectedBackground': '#f2d9a8',
      'editorSuggestWidget.highlightForeground': '#b45f06',
      'editorIndentGuide.background1': '#e4dac6',
      'editorIndentGuide.activeBackground1': '#cfc0a5',
    },
  });
}

/* ------------------------------------------------------------------ */
/* Java autocompletion: keywords, snippets, stdlib member completions.  */
/* ------------------------------------------------------------------ */

const JAVA_KEYWORDS = [
  'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
  'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
  'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
  'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new',
  'package', 'private', 'protected', 'public', 'return', 'short', 'static',
  'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
  'transient', 'try', 'var', 'void', 'volatile', 'while',
];

const JAVA_LITERALS = ['true', 'false', 'null'];

interface Snippet {
  label: string;
  detail: string;
  doc: string;
  insert: string;
}

const SNIPPETS: Snippet[] = [
  {
    label: 'fori',
    detail: 'snippet · indexed for loop',
    doc: 'Classic indexed `for` loop with tab stops on the counter, bound and body.',
    insert: 'for (int ${1:i} = 0; ${1:i} < ${2:n}; ${1:i}++) {\n\t$0\n}',
  },
  {
    label: 'foreach',
    detail: 'snippet · enhanced for loop',
    doc: 'Enhanced for-each loop over a collection or array.',
    insert: 'for (${1:String} ${2:item} : ${3:items}) {\n\t$0\n}',
  },
  {
    label: 'while',
    detail: 'snippet · while loop',
    doc: '`while` loop with the condition selected first.',
    insert: 'while (${1:condition}) {\n\t$0\n}',
  },
  {
    label: 'if',
    detail: 'snippet · if statement',
    doc: '`if` statement with the condition selected first.',
    insert: 'if (${1:condition}) {\n\t$0\n}',
  },
  {
    label: 'ifelse',
    detail: 'snippet · if / else',
    doc: '`if` / `else` block with tab stops on condition, both bodies.',
    insert: 'if (${1:condition}) {\n\t$2\n} else {\n\t$0\n}',
  },
  {
    label: 'sout',
    detail: 'snippet · System.out.println',
    doc: 'Print a line to stdout. The expression is selected for typing.',
    insert: 'System.out.println($1);$0',
  },
  {
    label: 'psvm',
    detail: 'snippet · main method',
    doc: '`public static void main(String[] args)` entry point.',
    insert: 'public static void main(String[] args) {\n\t$0\n}',
  },
  {
    label: 'trycatch',
    detail: 'snippet · try / catch',
    doc: '`try` / `catch` block with tab stops on the body, exception type and name.',
    insert: 'try {\n\t$1\n} catch (${2:Exception} ${3:e}) {\n\t$0\n}',
  },
];

interface Member {
  /** e.g. "charAt(int index)" */
  label: string;
  /** e.g. "String → char" */
  detail: string;
  /** e.g. "charAt(int index) : char" */
  sig: string;
  doc: string;
  /** snippet insert text */
  insert: string;
}

function m(
  label: string,
  detail: string,
  sig: string,
  doc: string,
  insert?: string,
): Member {
  return { label, detail, sig, doc, insert: insert ?? `${label.split('(')[0]}()` };
}

const MEMBERS: Record<string, Member[]> = {
  String: [
    m('length()', 'String → int', 'length() : int', 'Returns the number of characters in this string.'),
    m('charAt(int index)', 'String → char', 'charAt(int index) : char', 'Returns the char at the given index.', 'charAt(${1:index})$0'),
    m('substring(int begin)', 'String → String', 'substring(int begin) : String', 'Returns the substring from begin to the end.', 'substring(${1:begin})$0'),
    m('substring(int begin, int end)', 'String → String', 'substring(int begin, int end) : String', 'Returns the substring from begin (inclusive) to end (exclusive).', 'substring(${1:begin}, ${2:end})$0'),
    m('indexOf(String s)', 'String → int', 'indexOf(String s) : int', 'Index of the first occurrence, or -1.', 'indexOf(${1:s})$0'),
    m('lastIndexOf(String s)', 'String → int', 'lastIndexOf(String s) : int', 'Index of the last occurrence, or -1.', 'lastIndexOf(${1:s})$0'),
    m('contains(CharSequence s)', 'String → boolean', 'contains(CharSequence s) : boolean', 'True if this string contains the sequence.', 'contains(${1:s})$0'),
    m('startsWith(String prefix)', 'String → boolean', 'startsWith(String prefix) : boolean', 'True if this string starts with the prefix.', 'startsWith(${1:prefix})$0'),
    m('endsWith(String suffix)', 'String → boolean', 'endsWith(String suffix) : boolean', 'True if this string ends with the suffix.', 'endsWith(${1:suffix})$0'),
    m('equals(Object o)', 'String → boolean', 'equals(Object o) : boolean', 'Compares string contents (not references).', 'equals(${1:o})$0'),
    m('equalsIgnoreCase(String s)', 'String → boolean', 'equalsIgnoreCase(String s) : boolean', 'Content comparison ignoring case.', 'equalsIgnoreCase(${1:s})$0'),
    m('isEmpty()', 'String → boolean', 'isEmpty() : boolean', 'True if length() == 0.'),
    m('isBlank()', 'String → boolean', 'isBlank() : boolean', 'True if empty or only whitespace (Java 11+).'),
    m('toLowerCase()', 'String → String', 'toLowerCase() : String', 'Lower-cased copy of this string.'),
    m('toUpperCase()', 'String → String', 'toUpperCase() : String', 'Upper-cased copy of this string.'),
    m('trim()', 'String → String', 'trim() : String', 'Copy with leading/trailing whitespace removed.'),
    m('split(String regex)', 'String → String[]', 'split(String regex) : String[]', 'Splits around matches of the regex.', 'split(${1:regex})$0'),
    m('replace(char old, char new)', 'String → String', 'replace(char old, char new) : String', 'Copy with every old char replaced.', 'replace(${1:oldChar}, ${2:newChar})$0'),
    m('toCharArray()', 'String → char[]', 'toCharArray() : char[]', 'Converts this string to a new char array.'),
  ],
  StringBuilder: [
    m('append(...)', 'StringBuilder → StringBuilder', 'append(x) : StringBuilder', 'Appends the argument and returns this builder (chainable).', 'append(${1:x})$0'),
    m('toString()', 'StringBuilder → String', 'toString() : String', 'Returns the built string.'),
    m('reverse()', 'StringBuilder → StringBuilder', 'reverse() : StringBuilder', 'Reverses the character sequence in place.'),
    m('length()', 'StringBuilder → int', 'length() : int', 'Number of characters currently in the builder.'),
    m('charAt(int index)', 'StringBuilder → char', 'charAt(int index) : char', 'Char at the given index.', 'charAt(${1:index})$0'),
    m('setCharAt(int index, char c)', 'StringBuilder → void', 'setCharAt(int index, char c) : void', 'Replaces the char at the index.', 'setCharAt(${1:index}, ${2:c})$0'),
    m('delete(int start, int end)', 'StringBuilder → StringBuilder', 'delete(int start, int end) : StringBuilder', 'Removes chars from start (inclusive) to end (exclusive).', 'delete(${1:start}, ${2:end})$0'),
    m('insert(int offset, ...)', 'StringBuilder → StringBuilder', 'insert(int offset, x) : StringBuilder', 'Inserts the argument at the offset.', 'insert(${1:offset}, ${2:x})$0'),
  ],
  List: [
    m('add(E e)', 'List → boolean', 'add(E e) : boolean', 'Appends the element to the end.', 'add(${1:e})$0'),
    m('add(int index, E e)', 'List → void', 'add(int index, E e) : void', 'Inserts the element at the index.', 'add(${1:index}, ${2:e})$0'),
    m('get(int index)', 'List → E', 'get(int index) : E', 'Returns the element at the index.', 'get(${1:index})$0'),
    m('set(int index, E e)', 'List → E', 'set(int index, E e) : E', 'Replaces the element, returning the old one.', 'set(${1:index}, ${2:e})$0'),
    m('remove(int index)', 'List → E', 'remove(int index) : E', 'Removes and returns the element at the index.', 'remove(${1:index})$0'),
    m('remove(Object o)', 'List → boolean', 'remove(Object o) : boolean', 'Removes the first occurrence of o.', 'remove(${1:o})$0'),
    m('size()', 'List → int', 'size() : int', 'Number of elements.'),
    m('isEmpty()', 'List → boolean', 'isEmpty() : boolean', 'True if size() == 0.'),
    m('contains(Object o)', 'List → boolean', 'contains(Object o) : boolean', 'True if the list contains o.', 'contains(${1:o})$0'),
    m('indexOf(Object o)', 'List → int', 'indexOf(Object o) : int', 'First index of o, or -1.', 'indexOf(${1:o})$0'),
    m('clear()', 'List → void', 'clear() : void', 'Removes all elements.'),
    m('sort(Comparator)', 'List → void', 'sort(Comparator<? super E> c) : void', 'Sorts in place using the comparator.', 'sort(${1:comparator})$0'),
    m('toArray()', 'List → Object[]', 'toArray() : Object[]', 'Returns an array containing the elements.'),
  ],
  Map: [
    m('put(K key, V value)', 'Map → V', 'put(K key, V value) : V', 'Associates value with key, returning the old value (or null).', 'put(${1:key}, ${2:value})$0'),
    m('get(Object key)', 'Map → V', 'get(Object key) : V', 'Value for the key, or null if absent.', 'get(${1:key})$0'),
    m('getOrDefault(Object key, V def)', 'Map → V', 'getOrDefault(Object key, V defaultValue) : V', 'Value for the key, or defaultValue if absent.', 'getOrDefault(${1:key}, ${2:defaultValue})$0'),
    m('containsKey(Object key)', 'Map → boolean', 'containsKey(Object key) : boolean', 'True if the key is present.', 'containsKey(${1:key})$0'),
    m('containsValue(Object v)', 'Map → boolean', 'containsValue(Object value) : boolean', 'True if some key maps to value.', 'containsValue(${1:value})$0'),
    m('remove(Object key)', 'Map → V', 'remove(Object key) : V', 'Removes the mapping, returning the old value.', 'remove(${1:key})$0'),
    m('keySet()', 'Map → Set<K>', 'keySet() : Set<K>', 'Set view of the keys.'),
    m('values()', 'Map → Collection<V>', 'values() : Collection<V>', 'Collection view of the values.'),
    m('entrySet()', 'Map → Set<Entry>', 'entrySet() : Set<Map.Entry<K,V>>', 'Set view of key-value entries — ideal for iteration.'),
    m('putIfAbsent(K key, V value)', 'Map → V', 'putIfAbsent(K key, V value) : V', 'Puts only if the key is absent; returns the existing value or null.', 'putIfAbsent(${1:key}, ${2:value})$0'),
    m('size()', 'Map → int', 'size() : int', 'Number of mappings.'),
    m('isEmpty()', 'Map → boolean', 'isEmpty() : boolean', 'True if size() == 0.'),
    m('clear()', 'Map → void', 'clear() : void', 'Removes all mappings.'),
  ],
  Set: [
    m('add(E e)', 'Set → boolean', 'add(E e) : boolean', 'Adds the element if not already present.', 'add(${1:e})$0'),
    m('contains(Object o)', 'Set → boolean', 'contains(Object o) : boolean', 'True if the set contains o.', 'contains(${1:o})$0'),
    m('remove(Object o)', 'Set → boolean', 'remove(Object o) : boolean', 'Removes o if present.', 'remove(${1:o})$0'),
    m('size()', 'Set → int', 'size() : int', 'Number of elements.'),
    m('isEmpty()', 'Set → boolean', 'isEmpty() : boolean', 'True if size() == 0.'),
    m('clear()', 'Set → void', 'clear() : void', 'Removes all elements.'),
  ],
  Arrays: [
    m('sort(int[] a)', 'Arrays → void', 'Arrays.sort(int[] a) : void', 'Sorts the array in ascending order (static).', 'sort(${1:a})$0'),
    m('sort(int[] a, int from, int to)', 'Arrays → void', 'Arrays.sort(int[] a, int from, int to) : void', 'Sorts the range [from, to) in place.', 'sort(${1:a}, ${2:from}, ${3:to})$0'),
    m('toString(int[] a)', 'Arrays → String', 'Arrays.toString(int[] a) : String', 'Human-readable form like "[1, 2, 3]".', 'toString(${1:a})$0'),
    m('asList(T... a)', 'Arrays → List<T>', 'Arrays.asList(T... a) : List<T>', 'Fixed-size list view backed by the array.', 'asList(${1:a})$0'),
    m('binarySearch(int[] a, int key)', 'Arrays → int', 'Arrays.binarySearch(int[] a, int key) : int', 'Binary search on a SORTED array; index or negative insertion point.', 'binarySearch(${1:a}, ${2:key})$0'),
    m('fill(int[] a, int val)', 'Arrays → void', 'Arrays.fill(int[] a, int val) : void', 'Sets every element to val.', 'fill(${1:a}, ${2:val})$0'),
    m('equals(int[] a, int[] b)', 'Arrays → boolean', 'Arrays.equals(int[] a, int[] b) : boolean', 'True if both arrays hold the same elements in order.', 'equals(${1:a}, ${2:b})$0'),
    m('copyOf(int[] a, int len)', 'Arrays → int[]', 'Arrays.copyOf(int[] a, int newLength) : int[]', 'Copies the array, truncating or padding with zeros.', 'copyOf(${1:a}, ${2:newLength})$0'),
  ],
  Collections: [
    m('sort(List<T> list)', 'Collections → void', 'Collections.sort(List<T> list) : void', 'Sorts the list into ascending order (static).', 'sort(${1:list})$0'),
    m('reverse(List<?> list)', 'Collections → void', 'Collections.reverse(List<?> list) : void', 'Reverses the list in place.', 'reverse(${1:list})$0'),
    m('max(Collection)', 'Collections → T', 'Collections.max(Collection<? extends T> c) : T', 'The maximum element (natural ordering).', 'max(${1:c})$0'),
    m('min(Collection)', 'Collections → T', 'Collections.min(Collection<? extends T> c) : T', 'The minimum element (natural ordering).', 'min(${1:c})$0'),
    m('swap(List<?> list, int i, int j)', 'Collections → void', 'Collections.swap(List<?> list, int i, int j) : void', 'Swaps the elements at i and j.', 'swap(${1:list}, ${2:i}, ${3:j})$0'),
    m('shuffle(List<?> list)', 'Collections → void', 'Collections.shuffle(List<?> list) : void', 'Randomly permutes the list.', 'shuffle(${1:list})$0'),
  ],
  Math: [
    m('max(int a, int b)', 'Math → int', 'Math.max(int a, int b) : int', 'The greater of the two (static).', 'max(${1:a}, ${2:b})$0'),
    m('min(int a, int b)', 'Math → int', 'Math.min(int a, int b) : int', 'The smaller of the two (static).', 'min(${1:a}, ${2:b})$0'),
    m('abs(int a)', 'Math → int', 'Math.abs(int a) : int', 'Absolute value.', 'abs(${1:a})$0'),
    m('pow(double a, double b)', 'Math → double', 'Math.pow(double a, double b) : double', 'a raised to the power b.', 'pow(${1:a}, ${2:b})$0'),
    m('sqrt(double a)', 'Math → double', 'Math.sqrt(double a) : double', 'Square root.', 'sqrt(${1:a})$0'),
  ],
};

/** Light receiver-name heuristic so the most likely type's members sort first. */
function guessType(receiver: string): string | null {
  if (/^(str|s|name|text|word|line|key|val|t)$/i.test(receiver)) return 'String';
  if (/^(sb|builder|buffer)$/i.test(receiver)) return 'StringBuilder';
  if (/^(list|nums|arr|res|ans|out|items|vals|a|b)$/i.test(receiver)) return 'List';
  if (/^(map|freq|counts|count|memo|cache|dp|index|pos)$/i.test(receiver)) return 'Map';
  if (/^(set|seen|visited|unique)$/i.test(receiver)) return 'Set';
  if (receiver === 'Arrays') return 'Arrays';
  if (receiver === 'Collections') return 'Collections';
  if (receiver === 'Math') return 'Math';
  return null;
}

let completionRegistered = false;

export function registerJavaCompletions(monaco: Monaco): void {
  if (completionRegistered) return;
  completionRegistered = true;
  monaco.languages.registerCompletionItemProvider(
    'java',
    buildJavaProvider(monaco),
  );
}

/* The provider object, typed explicitly so model/position infer correctly. */
function buildJavaProvider(
  monaco: Monaco,
): monacoTypes.languages.CompletionItemProvider {
  return {
    triggerCharacters: ['.'],
    provideCompletionItems(model, position) {
      const linePrefix = model.getValueInRange({
        startLineNumber: position.lineNumber,
        startColumn: 1,
        endLineNumber: position.lineNumber,
        endColumn: position.column,
      });
      const word = model.getWordUntilPosition(position);
      const range = new monaco.Range(
        position.lineNumber,
        word.startColumn,
        position.lineNumber,
        position.column,
      );

      // ---- after a dot: stdlib member completions ------------------
      const dotMatch = /([A-Za-z_$][\w$]*)\.([\w$]*)$/.exec(linePrefix);
      if (dotMatch) {
        const guessed = guessType(dotMatch[1]);
        const suggestions: monacoTypes.languages.CompletionItem[] = [];
        for (const [typeName, members] of Object.entries(MEMBERS)) {
          for (const mb of members) {
            suggestions.push({
              label: mb.label,
              kind: monaco.languages.CompletionItemKind.Method,
              detail: mb.detail,
              documentation: {
                value: `**${mb.sig}**\n\n${mb.doc}`,
              } as monacoTypes.IMarkdownString,
              insertText: mb.insert,
              insertTextRules:
                monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
              range,
              sortText: `${typeName === guessed ? '0' : '1'}_${typeName}_${mb.label}`,
              filterText: mb.label,
            });
          }
        }
        return { suggestions };
      }

      // ---- plain word context: snippets first, then keywords --------
      const suggestions: monacoTypes.languages.CompletionItem[] = [
        ...SNIPPETS.map(
          (s): monacoTypes.languages.CompletionItem => ({
            label: s.label,
            kind: monaco.languages.CompletionItemKind.Snippet,
            detail: s.detail,
            documentation: { value: s.doc } as monacoTypes.IMarkdownString,
            insertText: s.insert,
            insertTextRules:
              monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            range,
            sortText: `0_${s.label}`,
          }),
        ),
        ...JAVA_KEYWORDS.map(
          (kw): monacoTypes.languages.CompletionItem => ({
            label: kw,
            kind: monaco.languages.CompletionItemKind.Keyword,
            detail: 'keyword',
            insertText: kw,
            range,
            sortText: `1_${kw}`,
          }),
        ),
        ...JAVA_LITERALS.map(
          (lit): monacoTypes.languages.CompletionItem => ({
            label: lit,
            kind: monaco.languages.CompletionItemKind.Keyword,
            detail: 'literal',
            insertText: lit,
            range,
            sortText: `1_${lit}`,
          }),
        ),
      ];
      return { suggestions };
    },
  };
}
