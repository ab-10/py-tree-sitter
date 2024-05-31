from collections.abc import ByteString, Callable, Iterator, Sequence
from typing import Annotated, Any, Final, Literal, NamedTuple, Protocol, Self, final, overload

class Point(NamedTuple):
    row: int
    column: int

@final
class Language:
    def __init__(self, ptr: Annotated[int | object, "TSLanguage *"], /) -> None: ...

    # TODO(0.24): implement name
    # @property
    # def name(self) -> str | None: ...

    @property
    def version(self) -> int: ...
    @property
    def node_kind_count(self) -> int: ...
    @property
    def parse_state_count(self) -> int: ...
    @property
    def field_count(self) -> int: ...
    def node_kind_for_id(self, id: int, /) -> str | None: ...
    def id_for_node_kind(self, kind: str, named: bool, /) -> int | None: ...
    def node_kind_is_named(self, id: int, /) -> bool: ...
    def node_kind_is_visible(self, id: int, /) -> bool: ...
    def field_name_for_id(self, field_id: int, /) -> str | None: ...
    def field_id_for_name(self, name: str, /) -> int | None: ...
    def next_state(self, state: int, id: int, /) -> int: ...
    def lookahead_iterator(self, state: int, /) -> LookaheadIterator | None: ...
    def query(self, source: str, /) -> Query: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: Any, /) -> bool: ...
    def __ne__(self, other: Any, /) -> bool: ...
    def __hash__(self) -> int: ...

@final
class Node:
    @property
    def id(self) -> int: ...
    @property
    def kind_id(self) -> int: ...
    @property
    def grammar_id(self) -> int: ...
    @property
    def grammar_name(self) -> str: ...
    @property
    def type(self) -> str: ...
    @property
    def is_named(self) -> bool: ...
    @property
    def is_extra(self) -> bool: ...
    @property
    def has_changes(self) -> bool: ...
    @property
    def has_error(self) -> bool: ...
    @property
    def is_error(self) -> bool: ...
    @property
    def parse_state(self) -> int: ...
    @property
    def next_parse_state(self) -> int: ...
    @property
    def is_missing(self) -> bool: ...
    @property
    def start_byte(self) -> int: ...
    @property
    def end_byte(self) -> int: ...
    @property
    def byte_range(self) -> tuple[int, int]: ...
    @property
    def range(self) -> Range: ...
    @property
    def start_point(self) -> Point: ...
    @property
    def end_point(self) -> Point: ...
    @property
    def children(self) -> list[Node]: ...
    @property
    def child_count(self) -> int: ...
    @property
    def named_children(self) -> list[Node]: ...
    @property
    def named_child_count(self) -> int: ...
    @property
    def parent(self) -> Node | None: ...
    @property
    def next_sibling(self) -> Node | None: ...
    @property
    def prev_sibling(self) -> Node | None: ...
    @property
    def next_named_sibling(self) -> Node | None: ...
    @property
    def prev_named_sibling(self) -> Node | None: ...
    @property
    def descendant_count(self) -> int: ...
    @property
    def text(self) -> bytes | None: ...
    def walk(self) -> TreeCursor: ...
    def edit(
        self,
        start_byte: int,
        old_end_byte: int,
        new_end_byte: int,
        start_point: Point | tuple[int, int],
        old_end_point: Point | tuple[int, int],
        new_end_point: Point | tuple[int, int],
    ) -> None: ...
    def child(self, index: int, /) -> Node | None: ...
    def named_child(self, index: int, /) -> Node | None: ...
    def child_by_field_id(self, id: int, /) -> Node | None: ...
    def child_by_field_name(self, name: str, /) -> Node | None: ...
    def child_containing_descendant(self, descendant: Node, /) -> Node | None: ...
    def children_by_field_id(self, id: int, /) -> list[Node]: ...
    def children_by_field_name(self, name: str, /) -> list[Node]: ...
    def field_name_for_child(self, child_index: int, /) -> str | None: ...
    def descendant_for_byte_range(
        self,
        start_byte: int,
        end_byte: int,
        /,
    ) -> Node | None: ...
    def named_descendant_for_byte_range(
        self,
        start_byte: int,
        end_byte: int,
        /,
    ) -> Node | None: ...
    def descendant_for_point_range(
        self,
        start_point: Point | tuple[int, int],
        end_point: Point | tuple[int, int],
        /,
    ) -> Node | None: ...
    def named_descendant_for_point_range(
        self,
        start_point: Point | tuple[int, int],
        end_point: Point | tuple[int, int],
        /,
    ) -> Node | None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __eq__(self, other: Any, /) -> bool: ...
    def __ne__(self, other: Any, /) -> bool: ...
    def __hash__(self) -> int: ...

@final
class Tree:
    @property
    def root_node(self) -> Node: ...
    @property
    def included_ranges(self) -> list[Range]: ...
    @property
    def language(self) -> Language: ...
    def root_node_with_offset(
        self,
        offset_bytes: int,
        offset_extent: Point | tuple[int, int],
        /,
    ) -> Node | None: ...
    def edit(
        self,
        start_byte: int,
        old_end_byte: int,
        new_end_byte: int,
        start_point: Point | tuple[int, int],
        old_end_point: Point | tuple[int, int],
        new_end_point: Point | tuple[int, int],
    ) -> None: ...
    def walk(self) -> TreeCursor: ...
    def changed_ranges(self, new_tree: Tree) -> list[Range]: ...
    # TODO(0.24): add print_dot_graph
    # TODO(0.24): add copy methods

@final
class TreeCursor:
    @property
    def node(self) -> Node | None: ...
    @property
    def field_id(self) -> int | None: ...
    @property
    def field_name(self) -> str | None: ...
    @property
    def depth(self) -> int: ...
    @property
    def descendant_index(self) -> int: ...
    def copy(self) -> TreeCursor: ...
    def reset(self, node: Node, /) -> None: ...
    def reset_to(self, cursor: TreeCursor, /) -> None: ...
    def goto_first_child(self) -> bool: ...
    def goto_last_child(self) -> bool: ...
    def goto_parent(self) -> bool: ...
    def goto_next_sibling(self) -> bool: ...
    def goto_previous_sibling(self) -> bool: ...
    def goto_descendant(self, index: int, /) -> None: ...
    def goto_first_child_for_byte(self, byte: int, /) -> int | None: ...
    def goto_first_child_for_point(self, point: Point | tuple[int, int], /) -> int | None: ...
    def __copy__(self) -> TreeCursor: ...

@final
class Parser:
    def __init__(
        self,
        language: Language | None = None,
        *,
        included_ranges: Sequence[Range] | None = None,
        timeout_micros: int | None = None,
    ) -> None: ...
    @property
    def language(self) -> Language | None: ...
    @language.setter
    def language(self, language: Language) -> None: ...
    @language.deleter
    def language(self) -> None: ...
    @property
    def included_ranges(self) -> list[Range]: ...
    @included_ranges.setter
    def included_ranges(self, ranges: Sequence[Range]) -> None: ...
    @included_ranges.deleter
    def included_ranges(self) -> None: ...
    @property
    def timeout_micros(self) -> int: ...
    @timeout_micros.setter
    def timeout_micros(self, timeout: int) -> None: ...
    @timeout_micros.deleter
    def timeout_micros(self) -> None: ...
    @overload
    def parse(
        self,
        source: ByteString,
        /,
        old_tree: Tree | None = None,
        encoding: Literal["utf8", "utf16"] = "utf8",
    ) -> Tree: ...
    @overload
    def parse(
        self,
        callback: Callable[[int, Point], bytes | None],
        /,
        old_tree: Tree | None = None,
        encoding: Literal["utf8", "utf16"] = "utf8",
    ) -> Tree: ...
    def reset(self) -> None: ...
    # TODO(0.24): add set_logger
    # TODO(0.24): add print_dot_graphs

@final
class QueryError(ValueError): ...

class QueryPredicate(Protocol):
    def __call__(
        self,
        predicate: str,
        args: list[tuple[str, Literal["capture", "string"]]],
        pattern_index: int,
        captures: dict[str, list[Node]]
    ) -> bool: ...

@final
class Query:
    def __init__(self, language: Language, source: str) -> None: ...
    @property
    def pattern_count(self) -> int: ...
    @property
    def capture_count(self) -> int: ...
    @property
    def match_limit(self) -> int: ...
    @property
    def did_exceed_match_limit(self) -> bool: ...
    def set_match_limit(self, match_limit: int | None) -> Self: ...
    def set_max_start_depth(self, max_start_depth: int | None) -> Self: ...
    def set_byte_range(self, byte_range: tuple[int, int] | None) -> Self: ...
    def set_point_range(
        self,
        point_range: tuple[Point | tuple[int, int], Point | tuple[int, int]] | None
    ) -> Self: ...
    def disable_pattern(self, index: int) -> Self: ...
    def disable_capture(self, capture: str) -> Self: ...
    def captures(
        self,
        node: Node,
        /,
        predicate: QueryPredicate | None = None
    ) -> dict[str, list[Node]]: ...
    def matches(
        self,
        node: Node,
        /,
        predicate: QueryPredicate | None = None
    ) -> list[tuple[int, dict[str, list[Node]]]]: ...
    def pattern_settings(self, index: int) -> dict[str, str | None]: ...
    def pattern_assertions(self, index: int) -> dict[str, tuple[str | None, bool]]: ...
    def start_byte_for_pattern(self, index: int) -> int: ...
    def is_pattern_rooted(self, index: int) -> bool: ...
    def is_pattern_non_local(self, index: int) -> bool: ...
    def is_pattern_guaranteed_at_step(self, offset: int) -> bool: ...

@final
class LookaheadIterator(Iterator[int]):
    @property
    def language(self) -> Language: ...
    @property
    def current_symbol(self) -> int: ...
    @property
    def current_symbol_name(self) -> str: ...

    # TODO(0.24): rename to reset
    def reset_state(self, state: int, language: Language | None = None) -> bool: ...
    def iter_names(self) -> Iterator[str]: ...

    # TODO(0.24): implement iter_symbols
    # def iter_symbols(self) -> Iterator[int]: ...

    # TODO(0.24): return tuple[int, str]
    def __next__(self) -> int: ...

@final
class Range:
    def __init__(
        self,
        start_point: Point | tuple[int, int],
        end_point: Point | tuple[int, int],
        start_byte: int,
        end_byte: int,
    ) -> None: ...
    @property
    def start_point(self) -> Point: ...
    @property
    def end_point(self) -> Point: ...
    @property
    def start_byte(self) -> int: ...
    @property
    def end_byte(self) -> int: ...
    def __eq__(self, other: Any, /) -> bool: ...
    def __ne__(self, other: Any, /) -> bool: ...
    def __repr__(self) -> str: ...
    def __hash__(self) -> int: ...

LANGUAGE_VERSION: Final[int]

MIN_COMPATIBLE_LANGUAGE_VERSION: Final[int]
