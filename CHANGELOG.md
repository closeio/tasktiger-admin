# Changes

## v0.4.3

* Keep the filter and the column sort of the queue list across page reloads.
  The page stores them in the URL query string (`filter`, `sort`, and
  `direction`), so you can also bookmark or share a filtered, sorted view.

## v0.4.2

* Make the task-state columns (Queued, Active, Scheduled, Error) sortable.
  Clicking a column header cycles its sort through descending, ascending, and
  the original order, with a `↓`/`↑` arrow showing the active direction.
  Grouped rows keep their children attached and sorted under their parent.

## v0.4.1

* First release with automated releases.